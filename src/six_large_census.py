"""Two exact six-only traversals beyond the bitmask boundary, with checkpoints."""
from pathlib import Path
import argparse, hashlib, json, subprocess, time
ROOT=Path(__file__).resolve().parents[1]
SOURCE=ROOT/'src/six_large_census.c'
BINARY=ROOT/'build/six_large_census'

def build():
    BINARY.parent.mkdir(exist_ok=True)
    if not BINARY.exists() or SOURCE.stat().st_mtime>BINARY.stat().st_mtime:
        subprocess.run(['cc','-std=c11','-O3','-Wall','-Wextra','-o',str(BINARY),str(SOURCE)],check=True)
    return BINARY

def run(n,mode):
    started=time.monotonic()
    result=subprocess.run([str(build()),str(n),mode],capture_output=True,text=True,check=True)
    families=sorted(sorted(tuple(map(int,p.split(','))) for p in line.split()) for line in result.stdout.splitlines())
    stats=json.loads(result.stderr.splitlines()[-1]);stats['wall_seconds']=round(time.monotonic()-started,3)
    assert len(families)==stats['families']
    assert sum(len(f)*(len(f)-1)//2 for f in families)==stats['pairs']
    return families,stats,result.stderr

def main():
    p=argparse.ArgumentParser();p.add_argument('--nmin',type=int,required=True);p.add_argument('--nmax',type=int,required=True)
    p.add_argument('--out',type=Path,default=ROOT/'results/2026-09-30-six-large-census');p.add_argument('--resume',action='store_true')
    a=p.parse_args();a.out.mkdir(parents=True,exist_ok=True)
    for n in range(a.nmin,a.nmax+1):
        path=a.out/f'n{n}.json'
        if a.resume and path.exists():
            old=json.loads(path.read_text());assert old['methods']==['C-gap-pairs','C-point-correlations'];print(f'n={n} resume',flush=True);continue
        print(f'n={n} start',flush=True)
        gap,gs,gl=run(n,'gap');print(gs,flush=True)
        point,ps,pl=run(n,'point');print(ps,flush=True)
        assert gap==point and gs['classes']==ps['classes'],n
        previous=ROOT/f'results/2026-09-30-six-census/n{n}.json'
        if previous.exists():
            known=json.loads(previous.read_text());assert gap==sorted(sorted(tuple(x) for x in f['members']) for f in known['families']),n
            assert gs['classes']==known['summary']['classes'],n
        from homometry import icv,dihedral_canon
        for family in gap:
            vectors={icv(s,n) for s in family};assert len(vectors)==1
            assert len(set(family))==len(family) and all(s==dihedral_canon(s,n) for s in family)
        rows=[dict(icv=list(icv(f[0],n)),members=f) for f in gap]
        result=dict(status='COMPUTED',methods=['C-gap-pairs','C-point-correlations'],summary=gs,independent=ps,families=rows,
                    source_sha256=hashlib.sha256(SOURCE.read_bytes()).hexdigest())
        temp=path.with_suffix('.tmp');temp.write_text(json.dumps(result,sort_keys=True)+'\n');temp.replace(path)
        (a.out/f'n{n}.log').write_text(gl+pl)
        print(f'n={n} independently agreed',flush=True)

if __name__=='__main__':main()
