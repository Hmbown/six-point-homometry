/* Exact six-only census for 6 <= n <= 255.
 * Independent modes: positive gap bracelets + pair distances, or all anchored
 * point subsets + directed membership correlations. No hash-only grouping.
 * Each record has the sorted fifteen distances (120 bits) and five points.
 * Output lines contain one family, its canonical tuples separated by spaces.
 * Neither mode uses unit multiplication. Memory ~24*C(n,6)/(2n) bytes.
 */
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>
typedef struct { uint64_t lo,hi,points; } record;
static record *records;
static size_t used,capacity;
static int n,mode,point[6],gap[6];

static void save(const unsigned char distance[15]) {
    if(used==capacity) {
        capacity=capacity?capacity+capacity/2:65536;
        records=realloc(records,capacity*sizeof(record));
        if(!records){fprintf(stderr,"allocation failed\n");exit(2);}
    }
    record r={0,0,0};
    for(int i=0;i<8;i++)r.lo|=(uint64_t)distance[i]<<(8*i);
    for(int i=8;i<15;i++)r.hi|=(uint64_t)distance[i]<<(8*(i-8));
    for(int i=1;i<6;i++)r.points|=(uint64_t)point[i]<<(8*(i-1));
    records[used++]=r;
}
static void pair_signature(void) {
    unsigned char ds[15];int z=0;
    for(int i=0;i<6;i++)for(int j=i+1;j<6;j++) {
        int d=point[j]-point[i];if(d>n-d)d=n-d;
        int k=z++;while(k && ds[k-1]>d){ds[k]=ds[k-1];k--;}
        ds[k]=(unsigned char)d;
    }
    save(ds);
}
static void correlation_signature(void) {
    unsigned char membership[255]={0},ds[15];int z=0;
    for(int i=0;i<6;i++)membership[point[i]]=1;
    for(int d=1;2*d<=n;d++) {
        int count=0;
        for(int i=0;i<6;i++){int x=point[i]+d;if(x>=n)x-=n;count+=membership[x];}
        if(2*d==n)count/=2;
        for(int j=0;j<count;j++)ds[z++]=(unsigned char)d;
    }
    if(z!=15){fprintf(stderr,"bad correlation mass\n");exit(3);}
    save(ds);
}
static int canonical_gaps(void) {
    for(int anchor=0;anchor<6;anchor++)for(int sign=-1;sign<=1;sign+=2) {
        for(int k=0;k<6;k++) {
            int j=(anchor+sign*k+12)%6;
            if(gap[j]<gap[k])return 0;
            if(gap[j]>gap[k])break;
        }
    }
    return 1;
}
static void gaps(int index,int left,int minimum) {
    if(index==5) {
        if(left<minimum)return;
        gap[5]=left;if(!canonical_gaps())return;
        point[0]=0;for(int i=1;i<6;i++)point[i]=point[i-1]+gap[i-1];
        pair_signature();return;
    }
    for(int g=minimum;g<=left-(5-index)*minimum;g++) {
        gap[index]=g;gaps(index+1,left-g,minimum);
    }
}
static int canonical_points(void) {
    /* Cyclic ordered points give sorted translated images without sorting.
       This traversal does not use or compare a gap vector. */
    for(int anchor=0;anchor<6;anchor++) {
        for(int k=1;k<6;k++) {
            int j=(anchor+k)%6,x=point[j]-point[anchor];if(x<0)x+=n;
            if(x<point[k])return 0;
            if(x>point[k])break;
        }
        for(int k=1;k<6;k++) {
            int j=(anchor-k+6)%6,x=point[anchor]-point[j];if(x<0)x+=n;
            if(x<point[k])return 0;
            if(x>point[k])break;
        }
    }
    return 1;
}
static void points(int index,int start) {
    if(index==6){if(canonical_points())correlation_signature();return;}
    for(int p=start;p<=n-(6-index);p++){point[index]=p;points(index+1,p+1);}
}
static int cmp(const void *aa,const void *bb) {
    const record *a=aa,*b=bb;
    if(a->hi!=b->hi)return a->hi<b->hi?-1:1;
    if(a->lo!=b->lo)return a->lo<b->lo?-1:1;
    return a->points<b->points?-1:a->points>b->points;
}
static void emit(uint64_t p) {
    printf("0");for(int i=0;i<5;i++)printf(",%u",(unsigned)((p>>(8*i))&255));
}
int main(int argc,char **argv) {
    if(argc!=3){fprintf(stderr,"usage: six_large_census n gap|point\n");return 1;}
    n=atoi(argv[1]);mode=strcmp(argv[2],"gap")?1:0;
    if(n<6||n>255||(mode&&strcmp(argv[2],"point")))return 1;
    clock_t begin=clock();
    if(mode){point[0]=0;points(1,1);}
    else for(int g=1;6*g<=n;g++){gap[0]=g;gaps(1,n-g,g);}
    double enumeration=(double)(clock()-begin)/CLOCKS_PER_SEC;
    fprintf(stderr,"enumerated n=%d mode=%s classes=%zu seconds=%.3f record_bytes=%zu\n",n,argv[2],used,enumeration,used*sizeof(record));
    qsort(records,used,sizeof(record),cmp);
    size_t families=0,pairs_count=0,largest=0;
    for(size_t i=0;i<used;) {
        size_t j=i+1;while(j<used&&records[i].lo==records[j].lo&&records[i].hi==records[j].hi)j++;
        if(j-i>1) {
            families++;pairs_count+=(j-i)*(j-i-1)/2;if(j-i>largest)largest=j-i;
            for(size_t k=i;k<j;k++){if(k>i)putchar(' ');emit(records[k].points);}putchar('\n');
        }
        i=j;
    }
    fprintf(stderr,"{\"n\":%d,\"mode\":\"%s\",\"classes\":%zu,\"families\":%zu,\"pairs\":%zu,\"largest\":%zu,\"seconds\":%.3f}\n",n,argv[2],used,families,pairs_count,largest,(double)(clock()-begin)/CLOCKS_PER_SEC);
    free(records);return 0;
}
