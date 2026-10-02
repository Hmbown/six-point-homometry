/*
 * fastcensus.c -- fast Z-family enumerator for Z_n (n <= 63), bitset based.
 *
 * Conventions (must match src/homometry.py exactly):
 *   - A set A subset Z_n is an n-bit word, bit i <-> element i.
 *   - Canonical form = lexicographically smallest SORTED TUPLE in the dihedral
 *     orbit.  For two k-sets X != Y (as bit words):  tuple(X) <lex tuple(Y)
 *     iff the lowest set bit of X^Y belongs to X.  (The first position where
 *     the sorted tuples differ is at the smallest element of the symmetric
 *     difference; whichever set contains it has the smaller entry there.)
 *   - ICV[d-1], d = 1..n/2, = #pairs at cyclic distance d
 *       = popcount(A & rot(A,d)) for d < n/2, and half that for d = n/2.
 *
 * Enumeration: canonical sets contain 0 and their first gap (e1 - 0) is the
 * minimum gap (otherwise translating a smaller-gap pair to 0 gives a
 * lexicographically smaller tuple).  We enumerate all k-subsets containing 0
 * whose gaps are all >= the first gap g, then run an exact canonicity test
 * (compare against every dihedral image that has 0 in it).  The pruning is
 * only a NECESSARY condition; the final test is exact, so the output is exactly
 * the set of canonical representatives.
 *
 * Grouping: records (hash(ICV), set) are sorted; runs of equal hash are split
 * by exact ICV comparison, so hash collisions can never merge families.
 * Optional --passes P: only records with hash % P == p are kept in pass p
 * (re-enumerating each pass), bounding memory.
 *
 * Complement: for |A| = k, ICV(A^c)[d] = ICV(A)[d] + n - 2k (d < n/2) and
 * ICV(A^c)[n/2] = ICV(A)[n/2] + n/2 - k; complementation commutes with the
 * dihedral action.  Hence A ~ B (homometric, distinct classes) iff A^c ~ B^c,
 * and the k-families map bijectively onto the (n-k)-families by complementing
 * each member and re-canonicalising.  With -c we also emit those families.
 *
 * Output (stdout), one family per line:  k <TAB> hex hex ...   (members sorted
 * by tuple-lex order).  Stats to stderr.
 *
 * usage: fastcensus n k [-t threads] [-P passes] [-c] [-q]
 *        -q : count only (no family output)
 */
#include <pthread.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>

typedef uint64_t u64;

static int N, K, NTHREADS = 14, PASSES = 1, CUR_PASS = 0, EMIT_COMP = 0, QUIET = 0;
static u64 MASK;

static inline u64 rotr(u64 x, int t) { /* element i -> i - t (mod N) */
    t %= N;
    if (t == 0) return x;
    return ((x >> t) | (x << (N - t))) & MASK;
}
static inline u64 rev(u64 x) { /* element i -> N-1-i */
    return __builtin_bitreverse64(x) >> (64 - N);
}
static inline int lexless(u64 a, u64 b) { /* tuple(a) < tuple(b) */
    u64 d = a ^ b;
    if (!d) return 0;
    return (a & (d & (~d + 1))) != 0;
}
/* exact canonicity test: x contains 0 */
static inline int is_canon(u64 x) {
    u64 y = x & (x - 1); /* skip t=0 */
    while (y) {
        int t = __builtin_ctzll(y);
        y &= y - 1;
        if (lexless(rotr(x, t), x)) return 0;
    }
    u64 r = rev(x);
    y = r;
    while (y) {
        int t = __builtin_ctzll(y);
        y &= y - 1;
        if (lexless(rotr(r, t), x)) return 0;
    }
    return 1;
}
static u64 canon(u64 x) {
    u64 best = 0;
    int first = 1;
    u64 y = x;
    while (y) {
        int t = __builtin_ctzll(y);
        y &= y - 1;
        u64 z = rotr(x, t);
        if (first || lexless(z, best)) { best = z; first = 0; }
    }
    u64 r = rev(x);
    y = r;
    while (y) {
        int t = __builtin_ctzll(y);
        y &= y - 1;
        u64 z = rotr(r, t);
        if (lexless(z, best)) best = z;
    }
    return best;
}
static inline void icv(u64 x, uint8_t *v) {
    int h = N / 2;
    for (int d = 1; d <= h; d++) {
        int c = __builtin_popcountll(x & rotr(x, d));
        if (2 * d == N) c /= 2;
        v[d - 1] = (uint8_t)c;
    }
}
static inline u64 icv_hash(u64 x) {
    u64 h = 1469598103934665603ULL;
    int hn = N / 2;
    for (int d = 1; d <= hn; d++) {
        u64 c = (u64)__builtin_popcountll(x & rotr(x, d));
        h ^= c + 0x9e3779b97f4a7c15ULL + (h << 6) + (h >> 2);
        h *= 1099511628211ULL;
    }
    h ^= h >> 33; h *= 0xff51afd7ed558ccdULL; h ^= h >> 33;
    return h;
}

typedef struct { u64 h, x; } rec_t;
typedef struct { rec_t *a; size_t n, cap; u64 leaves, canon; } buf_t;

static inline void push(buf_t *b, u64 h, u64 x) {
    if (b->n == b->cap) {
        b->cap = b->cap ? b->cap * 2 : (1 << 16);
        b->a = realloc(b->a, b->cap * sizeof(rec_t));
        if (!b->a) { fprintf(stderr, "out of memory\n"); exit(2); }
    }
    b->a[b->n].h = h; b->a[b->n].x = x; b->n++;
}

/* recursive enumeration: x has `placed` elements, last element at `last`,
 * min gap g.  Need (K - placed) more elements, each gap >= g, and final wrap
 * gap N - e_{K-1} >= g. */
static void rec(buf_t *b, u64 x, int placed, int last, int g) {
    if (placed == K) {
        if (N - last < g) return;
        b->leaves++;
        if (!is_canon(x)) return;
        b->canon++;
        if (QUIET) return;
        u64 h = icv_hash(x);
        if (PASSES > 1 && (int)(h % (u64)PASSES) != CUR_PASS) return;
        push(b, h, x);
        return;
    }
    int rem = K - placed; /* elements still to place, each needs gap g, plus wrap gap g */
    int maxe = N - rem * g; /* e <= N - (rem-1)*g - g */
    for (int e = last + g; e <= maxe; e++) rec(b, x | (1ULL << e), placed + 1, e, g);
}

/* work items: prefix (g, e2) where e1 = g */
typedef struct { int g, e2; } item_t;
static item_t *ITEMS; static int NITEMS; static int NEXT = 0;
static pthread_mutex_t MTX = PTHREAD_MUTEX_INITIALIZER;

static void *worker(void *arg) {
    buf_t *b = (buf_t *)arg;
    for (;;) {
        pthread_mutex_lock(&MTX);
        int i = NEXT++;
        pthread_mutex_unlock(&MTX);
        if (i >= NITEMS) break;
        item_t it = ITEMS[i];
        if (K == 2) { /* single item encodes e1 = g */
            rec(b, 1ULL | (1ULL << it.g), 2, it.g, it.g);
        } else {
            rec(b, 1ULL | (1ULL << it.g) | (1ULL << it.e2), 3, it.e2, it.g);
        }
    }
    return NULL;
}

static int cmp_rec(const void *p, const void *q) {
    const rec_t *a = p, *b = q;
    if (a->h != b->h) return a->h < b->h ? -1 : 1;
    if (a->x != b->x) return a->x < b->x ? -1 : 1;
    return 0;
}
static int CMPLEN;
typedef struct { uint8_t v[32]; u64 x; } irec_t;
static int cmp_irec(const void *p, const void *q) {
    const irec_t *a = p, *b = q;
    int c = memcmp(a->v, b->v, CMPLEN);
    if (c) return c;
    return lexless(a->x, b->x) ? -1 : (a->x == b->x ? 0 : 1);
}
static int cmp_lex(const void *p, const void *q) {
    u64 a = *(const u64 *)p, b = *(const u64 *)q;
    return lexless(a, b) ? -1 : (a == b ? 0 : 1);
}

static u64 NFAM = 0, MAXFAM = 0, HIST[1024];

static void emit(u64 *m, int cnt) {
    NFAM++;
    if ((u64)cnt > MAXFAM) MAXFAM = cnt;
    if (cnt < 1024) HIST[cnt]++;
    qsort(m, cnt, sizeof(u64), cmp_lex);
    printf("%d\t", K);
    for (int i = 0; i < cnt; i++) printf(i ? " %llx" : "%llx", (unsigned long long)m[i]);
    printf("\n");
    if (EMIT_COMP && 2 * K != N) {
        u64 cm[1024];
        for (int i = 0; i < cnt; i++) cm[i] = canon((~m[i]) & MASK);
        qsort(cm, cnt, sizeof(u64), cmp_lex);
        printf("%d\t", N - K);
        for (int i = 0; i < cnt; i++) printf(i ? " %llx" : "%llx", (unsigned long long)cm[i]);
        printf("\n");
    }
}

int main(int argc, char **argv) {
    if (argc < 3) { fprintf(stderr, "usage: fastcensus n k [-t T] [-P passes] [-c] [-q]\n"); return 1; }
    N = atoi(argv[1]); K = atoi(argv[2]);
    for (int i = 3; i < argc; i++) {
        if (!strcmp(argv[i], "-t")) NTHREADS = atoi(argv[++i]);
        else if (!strcmp(argv[i], "-P")) PASSES = atoi(argv[++i]);
        else if (!strcmp(argv[i], "-c")) EMIT_COMP = 1;
        else if (!strcmp(argv[i], "-q")) QUIET = 1;
    }
    if (N < 3 || N > 63 || K < 2 || K > N - 1) { fprintf(stderr, "bad n/k\n"); return 1; }
    MASK = (1ULL << N) - 1;
    CMPLEN = N / 2;
    /* build work items */
    ITEMS = malloc(sizeof(item_t) * (size_t)N * N);
    NITEMS = 0;
    for (int g = 1; g * K <= N; g++) {
        if (K == 2) { ITEMS[NITEMS].g = g; ITEMS[NITEMS].e2 = 0; NITEMS++; continue; }
        int rem = K - 2;
        int maxe = N - rem * g;
        for (int e2 = 2 * g; e2 <= maxe; e2++) { ITEMS[NITEMS].g = g; ITEMS[NITEMS].e2 = e2; NITEMS++; }
    }
    /* biggest items first (small g, small e2) is the natural order already */
    u64 total_leaves = 0, total_canon = 0, total_recs = 0;
    struct timespec t0, t1;
    clock_gettime(CLOCK_MONOTONIC, &t0);
    for (CUR_PASS = 0; CUR_PASS < PASSES; CUR_PASS++) {
        NEXT = 0;
        buf_t *bufs = calloc(NTHREADS, sizeof(buf_t));
        pthread_t *th = malloc(sizeof(pthread_t) * NTHREADS);
        for (int i = 0; i < NTHREADS; i++) pthread_create(&th[i], NULL, worker, &bufs[i]);
        for (int i = 0; i < NTHREADS; i++) pthread_join(th[i], NULL);
        size_t tot = 0;
        for (int i = 0; i < NTHREADS; i++) { tot += bufs[i].n; total_leaves += bufs[i].leaves; total_canon += bufs[i].canon; }
        total_recs += tot;
        if (!QUIET) {
            rec_t *all = malloc(sizeof(rec_t) * (tot ? tot : 1));
            size_t o = 0;
            for (int i = 0; i < NTHREADS; i++) { memcpy(all + o, bufs[i].a, bufs[i].n * sizeof(rec_t)); o += bufs[i].n; free(bufs[i].a); }
            qsort(all, tot, sizeof(rec_t), cmp_rec);
            size_t i = 0;
            while (i < tot) {
                size_t j = i + 1;
                while (j < tot && all[j].h == all[i].h) j++;
                if (j - i >= 2) {
                    size_t m = j - i;
                    irec_t *ir = malloc(sizeof(irec_t) * m);
                    for (size_t a = 0; a < m; a++) { memset(ir[a].v, 0, 32); icv(all[i + a].x, ir[a].v); ir[a].x = all[i + a].x; }
                    qsort(ir, m, sizeof(irec_t), cmp_irec);
                    size_t a = 0;
                    while (a < m) {
                        size_t b = a + 1;
                        while (b < m && !memcmp(ir[b].v, ir[a].v, CMPLEN)) b++;
                        if (b - a >= 2) {
                            if (b - a >= 1024) { fprintf(stderr, "family too large\n"); return 3; }
                            u64 mem[1024];
                            for (size_t c = a; c < b; c++) mem[c - a] = ir[c].x;
                            emit(mem, (int)(b - a));
                        }
                        a = b;
                    }
                    free(ir);
                }
                i = j;
            }
            free(all);
        }
        free(bufs); free(th);
    }
    clock_gettime(CLOCK_MONOTONIC, &t1);
    double sec = (t1.tv_sec - t0.tv_sec) + 1e-9 * (t1.tv_nsec - t0.tv_nsec);
    fprintf(stderr, "n=%d k=%d leaves=%llu classes=%llu families=%llu maxfam=%llu seconds=%.3f hist=",
            N, K, (unsigned long long)total_leaves, (unsigned long long)total_canon,
            (unsigned long long)NFAM, (unsigned long long)MAXFAM, sec);
    int firsth = 1;
    for (int i = 2; i < 1024; i++) if (HIST[i]) { fprintf(stderr, firsth ? "%d:%llu" : ",%d:%llu", i, (unsigned long long)HIST[i]); firsth = 0; }
    fprintf(stderr, "\n");
    fflush(stdout);
    return 0;
}
