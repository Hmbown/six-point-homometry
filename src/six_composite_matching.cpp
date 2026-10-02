// Exact labelled-point matching certificate for the two-parameter Bloom image.
// Integer arithmetic only; no modulus enumeration or subset census.
#include <algorithm>
#include <array>
#include <chrono>
#include <cstdint>
#include <fstream>
#include <iostream>
#include <map>
#include <numeric>
#include <sstream>
#include <string>
#include <vector>

using I = int64_t;
using Row = std::array<I, 2>;
using Mat = std::array<Row, 2>;
using Points = std::array<Row, 6>;
using Perm = std::array<int, 6>;
using Residual = std::array<Row, 10>;
using EndpointResidual = std::array<Row, 4>;
const Points X = {{{2,-4},{5,-4},{-4,-1},{-4,2},{2,2},{-1,5}}};
const Points Y = {{{-1,-4},{2,-4},{5,-1},{-4,2},{2,2},{-4,5}}};
const std::array<Row,12> lines = {{{1,0},{0,1},{1,-1},{1,1},{2,-1},{2,1},
                                 {3,-1},{1,-2},{1,2},{3,-2},{1,-3},{2,-3}}};
I det(Row a, Row b) { return a[0]*b[1]-a[1]*b[0]; }
Row primitive(Row r) {
    I g=std::gcd(r[0],r[1]);
    if(g==0) return r;
    r[0]/=g; r[1]/=g;
    if(r[0]<0 || (r[0]==0 && r[1]<0)) {r[0]=-r[0];r[1]=-r[1];}
    return r;
}
I largepart(I z) {
    z=std::abs(z);
    for(I p: {2,3,5,7}) while(z && z%p==0) z/=p;
    return z;
}
template<size_t N> I content(const std::array<Row,N>& h) {
    I d=0; for(auto r:h) {d=std::gcd(d,r[0]); d=std::gcd(d,r[1]);} return d;
}
template<size_t N> I minor_gcd(const std::array<Row,N>& h) {
    I d=0; for(size_t i=0;i<N;i++) for(size_t j=0;j<i;j++) d=std::gcd(d,det(h[i],h[j]));
    return d;
}
Mat multiply(Mat a,Mat b) {
    Mat c={}; for(int i=0;i<2;i++) for(int j=0;j<2;j++)
        for(int k=0;k<2;k++) c[i][j]+=a[i][k]*b[k][j]; return c;
}
std::vector<Mat> group() {
    Mat eye={{{1,0},{0,1}}},r={{{0,-1},{1,-1}}},t={{{0,1},{1,0}}};
    std::vector<Mat> out;
    for(int sign:{1,-1}) for(int j=0;j<2;j++) {Mat z=eye;
      for(int i=0;i<3;i++) {Mat q=j?multiply(z,t):z;
        for(auto &row:q)for(auto &c:row)c*=sign;out.push_back(q);z=multiply(r,z);}}
    return out;
}
Mat eliminated(int swap,int sx,const Perm& px) {
    const Points& u=swap?Y:X; Mat m={};
    for(int j=0;j<2;j++) {m[0][j]=sx*(-4*u[px[0]][j]+4*u[px[1]][j]);
                         m[1][j]=sx*(-5*u[px[0]][j]+2*u[px[1]][j]);} return m;
}
Residual residual(int swap,int sx,int sy,const Perm& px,const Perm& py,Mat m) {
    const Points& ux=swap?Y:X; const Points& uy=swap?X:Y; Residual h={};
    int z=0; for(int i=2;i<6;i++,z++) for(int j=0;j<2;j++)
        h[z][j]=X[i][0]*m[0][j]+X[i][1]*m[1][j]-12*sx*ux[px[i]][j];
    for(int i=0;i<6;i++,z++) for(int j=0;j<2;j++)
        h[z][j]=Y[i][0]*m[0][j]+Y[i][1]*m[1][j]-12*sy*uy[py[i]][j]; return h;
}
template<size_t N> void rows(std::ostream& o,const std::array<Row,N>& h) {
    o<<'[';for(size_t i=0;i<N;i++) {if(i)o<<',';o<<'['<<h[i][0]<<','<<h[i][1]<<']';}o<<']';
}
void perm(std::ostream& o,Perm p) {o<<'[';for(int i=0;i<6;i++){if(i)o<<',';o<<p[i];}o<<']';}
struct Stat {I count=0; int swap=0,sx=0,sy=0,px=0,py=0;Mat m={}; Residual h={};};
struct Exceptional {Stat s; int g=-1; I enlarged=0;};
void witness(std::ostream& o,const Stat& s,const std::vector<Perm>& p) {
    o<<"\"witness\":{\"swap\":"<<s.swap<<",\"sx\":"<<s.sx<<",\"sy\":"<<s.sy<<",\"px\":";
    perm(o,p[s.px]);o<<",\"py\":";perm(o,p[s.py]);o<<",\"M\":";rows(o,s.m);o<<",\"H\":";rows(o,s.h);o<<'}';
}
int endpoint_table(const std::string& path,const std::vector<Perm>& perms) {
    struct EndpointCase {int source,target,sign,index;Mat m;EndpointResidual h;};
    std::vector<EndpointCase> zero,one,exceptional;
    std::map<std::array<I,3>,I> hist1;std::map<std::array<I,2>,I> hist2;
    I count=0;
    for(int source=0;source<2;source++)for(int target=0;target<2;target++)for(int sign:{1,-1})for(int index=0;index<720;index++) {
        const Points& s=source?Y:X;const Points& t=target?Y:X;auto p=perms[index];
        Mat adj=source?Mat{{{-4,4},{-2,-1}}}:Mat{{{-4,4},{-5,2}}};Mat m={};
        for(int i=0;i<2;i++)for(int j=0;j<2;j++)m[i][j]=sign*(adj[i][0]*t[p[0]][j]+adj[i][1]*t[p[1]][j]);
        EndpointResidual h={};for(int i=2;i<6;i++)for(int j=0;j<2;j++)h[i-2][j]=s[i][0]*m[0][j]+s[i][1]*m[1][j]-12*sign*t[p[i]][j];
        I c=content(h),d=minor_gcd(h);EndpointCase e={source,target,sign,index,m,h};count++;
        if(c==0)zero.push_back(e);else if(d==0){Row dir={};for(auto r:h)if(r!=Row{0,0}){dir=primitive(r);break;}hist1[{dir[0],dir[1],c}]++;one.push_back(e);}
        else {hist2[{c,d}]++;if(largepart(d)>1)exceptional.push_back(e);}
    }
    std::ofstream o(path);o<<"{\"schema\":\"six-composite-single-endpoint-linear-v1\",\"status\":\"COMPUTED\",\"minimum_prime\":11,\"complete\":true,\"processed\":"<<count<<",\"rank0_count\":"<<zero.size()<<",\"rank1_count\":"<<one.size()<<",\"rank2_large_count\":"<<exceptional.size();
    auto emit=[&](const std::vector<EndpointCase>& cases){o<<'[';bool first=true;for(auto e:cases){if(!first)o<<',';first=false;o<<"{\"source\":"<<e.source<<",\"target\":"<<e.target<<",\"sign\":"<<e.sign<<",\"permutation\":";perm(o,perms[e.index]);o<<",\"M\":";rows(o,e.m);o<<",\"H\":";rows(o,e.h);o<<",\"content\":"<<content(e.h)<<",\"minor_gcd\":"<<minor_gcd(e.h)<<'}';}o<<']';};
    o<<",\"rank0\":";emit(zero);o<<",\"rank1_cases\":";emit(one);o<<",\"exceptional_cases\":";emit(exceptional);
    o<<",\"rank1\":[";bool first=true;for(auto [k,v]:hist1){if(!first)o<<',';first=false;o<<"{\"direction\":["<<k[0]<<','<<k[1]<<"],\"content\":"<<k[2]<<",\"count\":"<<v<<'}';}
    o<<"],\"rank2\":[";first=true;for(auto [k,v]:hist2){if(!first)o<<',';first=false;o<<"{\"content\":"<<k[0]<<",\"minor_gcd\":"<<k[1]<<",\"count\":"<<v<<'}';}o<<"]}";
    std::cerr<<"DONE endpoints="<<count<<" rank0="<<zero.size()<<" rank1="<<one.size()<<" exceptional="<<exceptional.size()<<'\n';return 0;
}
int main(int argc,char**argv) {
    std::string path="matching-certificate.json";I limit=4147200;bool endpoint=false;
    for(int i=1;i<argc;i++) {std::string a=argv[i];if(a=="--out"&&i+1<argc)path=argv[++i];
        else if(a=="--limit"&&i+1<argc)limit=std::stoll(argv[++i]);else if(a=="--endpoint")endpoint=true;else return 2;}
    std::vector<Perm> perms;Perm pp={{0,1,2,3,4,5}};do{perms.push_back(pp);}while(std::next_permutation(pp.begin(),pp.end()));
    if(endpoint)return endpoint_table(path,perms);
    auto gs=group();std::map<std::array<I,3>,Stat> rank1;
    std::map<std::array<I,2>,Stat> rank2;std::vector<Stat> rank0;
    std::map<std::string,Stat> problematic;std::vector<Exceptional> exceptions;I processed=0,rank2large=0,uncontained=0;
    auto started=std::chrono::steady_clock::now();
    bool done=false;
    for(int swap=0;swap<2&&!done;swap++)for(int sx:{1,-1})for(int sy:{1,-1})
      for(int ix=0;ix<720&&!done;ix++) {
        Mat m=eliminated(swap,sx,perms[ix]);
        for(int iy=0;iy<720;iy++) {
          if(processed>=limit){done=true;break;}processed++;
          auto h=residual(swap,sx,sy,perms[ix],perms[iy],m);
          I c=content(h),d=minor_gcd(h);Stat s;
          s.swap=swap;s.sx=sx;s.sy=sy;s.px=ix;s.py=iy;s.m=m;s.h=h;s.count=1;
          if(c==0)rank0.push_back(s);
          else if(d==0) {Row dir={};for(auto z:h)if(z!=Row{0,0}){dir=primitive(z);break;}
             auto& st=rank1[{dir[0],dir[1],c}];if(!st.count)st=s;else st.count++;
          } else {
             auto& st=rank2[{c,d}];if(!st.count)st=s;else st.count++;
             I lp=largepart(d);if(lp>1) {
               rank2large++; bool contained=false;
               for(int gi=0;gi<12;gi++) {auto g=gs[gi];I dg=d;std::array<Row,2> delta={};for(int i=0;i<2;i++)for(int j=0;j<2;j++)delta[i][j]=m[i][j]-12*g[i][j];
                 for(auto z:delta) for(auto r:h) dg=std::gcd(dg,det(z,r));
                 dg=std::gcd(dg,det(delta[0],delta[1]));
                 if(largepart(dg)==lp){contained=true;exceptions.push_back({s,gi,dg});break;}}
               if(!contained) {uncontained++;std::ostringstream key;key<<c<<':'<<d<<':';
                  for(auto r:h){auto pr=primitive(r);key<<pr[0]<<','<<pr[1]<<';';}
                  auto& bad=problematic[key.str()];if(!bad.count)bad=s;else bad.count++;}
             }
          }
        }
        if(ix%120==119)std::cerr<<"processed="<<processed<<" seconds="<<std::chrono::duration<double>(std::chrono::steady_clock::now()-started).count()<<'\n';
      }
    std::ofstream o(path);o<<"{\"schema\":\"six-composite-linear-matching-v1\",\"status\":\"COMPUTED\",\"minimum_prime\":11,\"complete\":"<<(processed==4147200?"true":"false")
      <<",\"processed\":"<<processed<<",\"rank0_count\":"<<rank0.size()<<",\"rank2_large_count\":"<<rank2large<<",\"uncontained_count\":"<<uncontained<<",\"rank0\":[";
    bool first=true;for(auto s:rank0){if(!first)o<<',';first=false;o<<'{';witness(o,s,perms);o<<'}';}o<<"],\"rank1\":[";first=true;
    for(auto [key,s]:rank1){if(!first)o<<',';first=false;o<<"{\"direction\":["<<key[0]<<','<<key[1]<<"],\"content\":"<<key[2]<<",\"count\":"<<s.count<<',';witness(o,s,perms);o<<'}';}
    o<<"],\"rank2\":[";first=true;for(auto [key,s]:rank2){if(!first)o<<',';first=false;o<<"{\"content\":"<<key[0]<<",\"minor_gcd\":"<<key[1]<<",\"count\":"<<s.count<<',';witness(o,s,perms);o<<'}';}
    o<<"],\"exceptional_cases\":[";first=true;for(auto e:exceptions){if(!first)o<<',';first=false;o<<"{\"g_index\":"<<e.g<<",\"g\":";rows(o,gs[e.g]);o<<",\"enlarged_minor_gcd\":"<<e.enlarged<<',';witness(o,e.s,perms);o<<'}';}
    o<<"],\"uncontained\":[";first=true;for(auto [key,s]:problematic){if(!first)o<<',';first=false;o<<"{\"count\":"<<s.count<<',';witness(o,s,perms);o<<'}';}
    o<<"]}";o.close();std::cerr<<"DONE processed="<<processed<<" rank0="<<rank0.size()<<" rank1_classes="<<rank1.size()<<" rank2_classes="<<rank2.size()<<" uncontained="<<uncontained
    <<" seconds="<<std::chrono::duration<double>(std::chrono::steady_clock::now()-started).count()<<'\n';return 0;
}
