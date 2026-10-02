/* Exact labelled-graph spanning-tree exhaustion, deliberately capped at k<=7.
 * Method 1: graph subsets and a Bareiss Laplacian cofactor determinant.
 * Method 2: Prufer sequences, adding each tree to every eligible supergraph.
 * No floating point, graph-isomorphism quotient, or sampled graph is used.
 * Checkpoint format: 8-byte magic, uint32 k/method, uint64 processed/length,
 * then uint32 counts indexed by the complete-graph edge bitmask. Native
 * little-endian integers are checked by the Python driver on this platform.
 */
#include <errno.h>
#include <inttypes.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>

enum { MAX_K = 7, BAREISS = 1, PRUEFER = 2 };
static const char MAGIC[8] = {'G','T','B','O','U','N','D','1'};
static uint64_t choose_table[22][22];
static int edge_a[21], edge_b[21], edge_index[7][7];

static void die(const char *message) {
    fprintf(stderr, "ERROR: %s\n", message);
    exit(2);
}

static uint64_t parse_number(const char *text) {
    char *end = NULL;
    if (!text[0] || text[0] == '-') die("expected nonnegative integer");
    errno = 0;
    uint64_t value = strtoull(text, &end, 10);
    if (errno || !end || *end) die("invalid integer argument");
    return value;
}

static double now(void) {
    struct timespec t;
    if (timespec_get(&t, TIME_UTC) != TIME_UTC) die("clock unavailable");
    return (double)t.tv_sec + (double)t.tv_nsec / 1e9;
}

static uint64_t power(uint64_t base, int exponent) {
    uint64_t result = 1;
    for (int i = 0; i < exponent; ++i) result *= base;
    return result;
}

static uint32_t next_combination(uint32_t mask) {
    uint32_t lowest = mask & (0u - mask);
    uint32_t raised = mask + lowest;
    return raised | (((raised ^ mask) >> 2) / lowest);
}

static void initialize(int k) {
    for (int n = 0; n <= 21; ++n) {
        choose_table[n][0] = choose_table[n][n] = 1;
        for (int r = 1; r < n; ++r)
            choose_table[n][r] = choose_table[n-1][r-1] + choose_table[n-1][r];
    }
    int index = 0;
    for (int a = 0; a < k; ++a)
        for (int b = a + 1; b < k; ++b) {
            edge_a[index] = a; edge_b[index] = b;
            edge_index[a][b] = edge_index[b][a] = index++;
        }
}

static uint32_t tree_determinant(int k, int edge_count, uint32_t graph) {
    int size = k - 1, sign = 1;
    int64_t a[6][6] = {{0}}, previous = 1;
    for (int e = 0; e < edge_count; ++e) if (graph & (1u << e)) {
        int u = edge_a[e], v = edge_b[e];
        if (u < size) ++a[u][u];
        if (v < size) ++a[v][v];
        if (u < size && v < size) { --a[u][v]; --a[v][u]; }
    }
    for (int pivot = 0; pivot < size - 1; ++pivot) {
        int row = pivot;
        while (row < size && a[row][pivot] == 0) ++row;
        if (row == size) return 0;
        if (row != pivot) {
            for (int column = 0; column < size; ++column) {
                int64_t t = a[row][column];
                a[row][column] = a[pivot][column]; a[pivot][column] = t;
            }
            sign = -sign;
        }
        int64_t value = a[pivot][pivot];
        for (int i = pivot + 1; i < size; ++i) {
            for (int j = pivot + 1; j < size; ++j) {
                int64_t numerator = value * a[i][j] - a[i][pivot] * a[pivot][j];
                if (previous == 0 || numerator % previous != 0)
                    die("Bareiss exact-division failure");
                a[i][j] = numerator / previous;
            }
            a[i][pivot] = 0;
        }
        previous = value;
    }
    int64_t determinant = sign * a[size-1][size-1];
    if (determinant < 0 || (uint64_t)determinant > power(k, k-2))
        die("tree determinant outside Cayley bound");
    return (uint32_t)determinant;
}

static uint32_t pruefer_tree(int k, uint64_t code) {
    int sequence[5], degrees[7], mask = 0;
    for (int vertex = 0; vertex < k; ++vertex) degrees[vertex] = 1;
    for (int position = 0; position < k - 2; ++position) {
        sequence[position] = (int)(code % (uint64_t)k); code /= (uint64_t)k;
        ++degrees[sequence[position]];
    }
    for (int position = 0; position < k - 2; ++position) {
        int leaf = 0;
        while (leaf < k && degrees[leaf] != 1) ++leaf;
        if (leaf == k) die("Prufer leaf missing");
        int neighbor = sequence[position];
        mask |= 1u << edge_index[leaf][neighbor];
        --degrees[leaf]; --degrees[neighbor];
    }
    int u = 0, v;
    while (degrees[u] != 1) ++u;
    v = u + 1;
    while (v < k && degrees[v] != 1) ++v;
    if (v == k) die("Prufer final edge missing");
    return (uint32_t)mask | (1u << edge_index[u][v]);
}

static void add_tree_supersets(int k, int edge_count, uint32_t tree,
                              uint32_t *counts) {
    uint32_t remaining_bits[21];
    int remaining = 0;
    for (int edge = 0; edge < edge_count; ++edge)
        if (!(tree & (1u << edge))) remaining_bits[remaining++] = 1u << edge;
    int added = k - 1;
    uint32_t selected = (1u << added) - 1;
    uint64_t total = choose_table[remaining][added];
    for (uint64_t index = 0; index < total; ++index) {
        uint32_t graph = tree, bits = selected;
        while (bits) {
            int bit = __builtin_ctz(bits);
            graph |= remaining_bits[bit];
            bits &= bits - 1;
        }
        ++counts[graph];
        if (index + 1 < total) selected = next_combination(selected);
    }
}

static void save_checkpoint(const char *path, uint32_t k, uint32_t method,
                            uint64_t processed, uint64_t length,
                            const uint32_t *counts) {
    char *temporary = malloc(strlen(path) + 5);
    if (!temporary) die("checkpoint pathname allocation failed");
    sprintf(temporary, "%s.tmp", path);
    FILE *file = fopen(temporary, "wb");
    if (!file) die("cannot open checkpoint temporary file");
    int ok = fwrite(MAGIC, 1, 8, file) == 8 &&
        fwrite(&k, 4, 1, file) == 1 && fwrite(&method, 4, 1, file) == 1 &&
        fwrite(&processed, 8, 1, file) == 1 && fwrite(&length, 8, 1, file) == 1 &&
        fwrite(counts, sizeof(*counts), (size_t)length, file) == length;
    if (fclose(file) != 0 || !ok) die("checkpoint write failed");
    if (rename(temporary, path) != 0) die("checkpoint rename failed");
    free(temporary);
}

static uint64_t load_checkpoint(const char *path, uint32_t k, uint32_t method,
                               uint64_t total, uint64_t length,
                               uint32_t *counts) {
    FILE *file = fopen(path, "rb");
    if (!file) {
        if (errno == ENOENT) return 0;
        die("cannot open checkpoint");
    }
    char magic[8]; uint32_t saved_k, saved_method;
    uint64_t processed, saved_length;
    int ok = fread(magic, 1, 8, file) == 8 && fread(&saved_k, 4, 1, file) == 1 &&
        fread(&saved_method, 4, 1, file) == 1 && fread(&processed, 8, 1, file) == 1 &&
        fread(&saved_length, 8, 1, file) == 1;
    if (!ok || memcmp(magic, MAGIC, 8) || saved_k != k || saved_method != method ||
        saved_length != length || processed > total) die("checkpoint header invalid");
    if (fread(counts, sizeof(*counts), (size_t)length, file) != length ||
        fgetc(file) != EOF) die("checkpoint payload length invalid");
    fclose(file);
    uint64_t cayley = power(k, (int)k-2);
    for (uint64_t i = 0; i < length; ++i)
        if (counts[i] > cayley) die("checkpoint count outside Cayley bound");
    return processed;
}

static void write_summary(const char *path, int k, int method, int edge_count,
                          uint64_t processed, uint64_t total, uint64_t resumed,
                          const uint32_t *counts, double seconds) {
    uint64_t cayley = power(k, k-2), graph_total = choose_table[edge_count][2*k-2];
    uint64_t *histogram = calloc((size_t)cayley+1, sizeof(*histogram));
    if (!histogram) die("histogram allocation failed");
    uint32_t selected = (1u << (2*k-2)) - 1, maximum = 0, example = selected;
    for (uint64_t index = 0; index < graph_total; ++index) {
        uint32_t count = counts[selected];
        if (count > cayley) die("histogram count outside Cayley bound");
        ++histogram[count];
        if (count > maximum) { maximum = count; example = selected; }
        if (index+1 < graph_total) selected = next_combination(selected);
    }
    FILE *file = fopen(path, "w");
    if (!file) die("cannot open summary");
    fprintf(file, "{\"vertices\":%d,\"graph_edges\":%d,\"labelled_graphs\":%" PRIu64
            ",\"complete_graph_trees\":%" PRIu64 ",\"method\":\"%s\","
            "\"processed\":%" PRIu64 ",\"total_items\":%" PRIu64
            ",\"resumed_from\":%" PRIu64 ",\"complete\":%s,\"seconds\":%.9f,"
            "\"superset_additions\":%" PRIu64 ",\"maximum\":%u,"
            "\"maximizer_count\":%" PRIu64 ",\"maximizing_graph_mask\":%u,\"histogram\":{",
            k, 2*k-2, graph_total, cayley, method == BAREISS ? "bareiss" : "pruefer",
            processed, total, resumed, processed == total ? "true" : "false", seconds,
            method == PRUEFER ? processed * choose_table[edge_count-k+1][k-1] : 0,
            maximum, histogram[maximum], example);
    int first = 1;
    for (uint32_t value = 0; value <= cayley; ++value) if (histogram[value]) {
        fprintf(file, "%s\"%u\":%" PRIu64, first ? "" : ",", value, histogram[value]);
        first = 0;
    }
    fprintf(file, "}}\n");
    if (fclose(file)) die("summary write failed");
    free(histogram);
}

int main(int argc, char **argv) {
    if (argc != 5 && argc != 6) {
        fprintf(stderr, "usage: %s k bareiss|pruefer checkpoint.bin summary.json [item_limit]\n", argv[0]);
        return 2;
    }
    uint64_t argument_k = parse_number(argv[1]);
    if (argument_k < 4 || argument_k > MAX_K) die("k must be in 4..7");
    int k = (int)argument_k, edge_count = k*(k-1)/2;
    int method = !strcmp(argv[2], "bareiss") ? BAREISS :
                 !strcmp(argv[2], "pruefer") ? PRUEFER : 0;
    if (!method) die("unknown method");
    uint64_t limit = argc == 6 ? parse_number(argv[5]) : UINT64_MAX;
    initialize(k);
    uint64_t length = 1ull << edge_count;
    uint64_t total = method == BAREISS ? choose_table[edge_count][2*k-2] : power(k, k-2);
    uint32_t *counts = calloc((size_t)length, sizeof(*counts));
    if (!counts) die("count table allocation failed");
    uint64_t processed = load_checkpoint(argv[3], (uint32_t)k, (uint32_t)method,
                                        total, length, counts), resumed = processed;
    uint64_t stop = limit > total-processed ? total : processed+limit;
    uint32_t graph = (1u << (2*k-2)) - 1;
    if (method == BAREISS)
        for (uint64_t index = 0; index < processed && index + 1 < total; ++index)
            graph = next_combination(graph);
    double started = now();
    fprintf(stderr, "START k=%d method=%s resumed=%" PRIu64 " total=%" PRIu64
            " limit=%" PRIu64 " table_bytes=%" PRIu64 "\n",
            k, argv[2], processed, total, stop-processed, length*sizeof(*counts));
    uint64_t interval = method == BAREISS ? 50000 : 1000;
    while (processed < stop) {
        if (method == BAREISS) {
            counts[graph] = tree_determinant(k, edge_count, graph);
            if (processed+1 < total) graph = next_combination(graph);
        } else {
            add_tree_supersets(k, edge_count, pruefer_tree(k, processed), counts);
        }
        ++processed;
        if (processed % interval == 0) {
            save_checkpoint(argv[3], (uint32_t)k, (uint32_t)method, processed, length, counts);
            fprintf(stderr, "PROGRESS k=%d method=%s processed=%" PRIu64
                    "/%" PRIu64 " seconds=%.6f checkpoint=saved\n",
                    k, argv[2], processed, total, now()-started);
        }
    }
    save_checkpoint(argv[3], (uint32_t)k, (uint32_t)method, processed, length, counts);
    double elapsed = now()-started;
    write_summary(argv[4], k, method, edge_count, processed, total, resumed, counts, elapsed);
    fprintf(stderr, "FINISH k=%d method=%s processed=%" PRIu64 "/%" PRIu64
            " seconds=%.6f complete=%s\n", k, argv[2], processed, total, elapsed,
            processed == total ? "true" : "false");
    free(counts);
    return 0;
}
