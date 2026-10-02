"""Run the exact six-point SMT input with an independent solver.

cvc5 Python wheel may be installed in a separate directory using pinned
.venv Python and selected by --module-dir; the project env is unchanged.
"""
import argparse,gzip,hashlib,json,sys,time
from pathlib import Path
p=argparse.ArgumentParser();p.add_argument('--module-dir');p.add_argument('--input',default='results/2026-09-30-six-integer-smt/count.smt2');p.add_argument('--out',default='results/2026-09-30-six-integer-smt/cvc5.json');p.add_argument('--timeout',type=int,default=60);a=p.parse_args()
if a.module_dir:sys.path.insert(0,a.module_dir)
import cvc5
s=cvc5.Solver();s.setOption('tlimit-per',str(a.timeout*1000));s.setOption('produce-proofs','true');s.setOption('check-proofs','true')
source=Path(a.input).read_text();source='\n'.join(line for line in source.splitlines() if ':timeout' not in line and 'all-statistics' not in line)
parser=cvc5.InputParser(s);parser.setStringInput(cvc5.InputLanguage.SMT_LIB_2_6,source,'six-integer');sm=parser.getSymbolManager();output=[];t=time.monotonic()
while True:
 cmd=parser.nextCommand()
 if cmd.isNull():break
 result=cmd.invoke(s,sm)
 if result.strip():
  if len(result)>10000:
   proof_path=Path(a.out).with_suffix('.proof.gz')
   with gzip.open(proof_path,'wt') as f:f.write(result)
   output.append({'proof_path':str(proof_path),'uncompressed_bytes':len(result.encode())})
  else:output.append(result.strip())
if not output or output[0] not in ('sat','unsat','unknown'):
 raise RuntimeError('No valid solver result: '+repr(output[:1]))
meta={'solver':'cvc5','version':cvc5.__version__,'proof_checking_enabled':True,'proofs_produced_and_internally_checked':output[0]=='unsat','seconds':time.monotonic()-t,'input':a.input,'source_sha256':hashlib.sha256(Path(a.input).read_bytes()).hexdigest(),'output':output,'status':'EXPERIMENTAL-SOLVER-RESULT'}
Path(a.out).write_text(json.dumps(meta,indent=2)+'\n');print(json.dumps(meta,indent=2))
