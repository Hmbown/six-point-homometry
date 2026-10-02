"""Exploratory exact SMT: six atoms counted with multiplicities on R."""
from pathlib import Path
import argparse,gzip,hashlib,json,subprocess,time
from six_integer_smt import encode
p=argparse.ArgumentParser();p.add_argument('--two',action='store_true');p.add_argument('--proof',action='store_true');p.add_argument('--timeout',type=int,default=60);p.add_argument('--out',default='results/2026-09-30-six-integer-weighted');a=p.parse_args()
s,meta=encode(timeout_ms=1000*a.timeout,normal_forms=a.two,proof=a.proof)
# Change only the ten adjacent coordinate inequalities. Lexicographic
# nonidentity stays strict, and diameter remains normalized to one.
for pts in [('0','a1','a2','a3','r','1'),('0','b1','b2','b3','r','1')]:
 for x,y in zip(pts,pts[1:]):s=s.replace(f'(assert (< {x} {y}))',f'(assert (<= {x} {y}))')
# A model is requested in a separate run only after SAT.
base=Path(a.out);base.mkdir(parents=True,exist_ok=True);path=base/'weighted.smt2';path.write_text(s)
t=time.monotonic();r=subprocess.run(['z3',str(path)],text=True,capture_output=True)
meta.update(status='EXPLORATORY',seconds=time.monotonic()-t,stdout=r.stdout,stderr=r.stderr,returncode=r.returncode,input_sha256=hashlib.sha256(s.encode()).hexdigest())
if a.proof:
 with gzip.open(base/'weighted.proof.gz','wt') as f:f.write(r.stdout)
 meta['stdout']=r.stdout.splitlines()[0]
 meta['proof_path']=str(base/'weighted.proof.gz')
(base/'weighted.json').write_text(json.dumps(meta,indent=2)+'\n');print(json.dumps(meta,indent=2))
