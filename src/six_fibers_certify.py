"""Attach integer row-lattice witnesses to low-fiber quotient DAGs.

The saved certificates can be checked using matrix multiplication only;
Hermite and Smith normal-form implementations are not verifier dependencies.
"""
from __future__ import annotations
import argparse,json
from pathlib import Path
from sympy import Matrix


def row_witness(source, target):
 """Return C with source = C target['matrix'] using its Smith witness."""
 m=Matrix(target['matrix']);u=Matrix(target['smith_u']);v=Matrix(target['smith_v'])
 diag=target['smith_diagonal'];rank=target['rank'];answer=[]
 for row in Matrix(source).tolist():
  z=Matrix([row])*v;coeff=[0]*m.rows
  assert all(z[i]==0 for i in range(rank,m.cols))
  for i in range(rank):
   assert z[i]%diag[i]==0
   coeff[i]=z[i]//diag[i]
  answer.append(list(Matrix([coeff])*u))
 c=Matrix(answer);assert c*m==Matrix(source)
 return c.tolist()


def certify(profile, directory):
 from six_fibers import edge_row,group_record
 r,s=profile
 cross=json.loads((directory/f'{r}-{s}-cross.json').read_text())
 dag=json.loads((directory/f'{r}-{s}-quotients.json').read_text())
 for root in dag['roots']:
  original=cross['records'][root['orbit_id']];canonical=dag['nodes'][root['node']]
  root['cross_to_root']=row_witness(original['matrix'],canonical)
  root['root_to_cross']=row_witness(canonical['matrix'],original)
 for node in dag['nodes']:
  if 'branches' not in node:continue
  ar=edge_row(node['chosen_a'],0)
  for branch in node['branches']:
   br=edge_row(branch['b_edge'],1);rel=[x-branch['sign']*y for x,y in zip(ar,br)]
   extension=group_record(Matrix(node['matrix']+[rel]));child=dag['nodes'][branch['child']]
   branch['extension_to_child']=row_witness(extension['matrix'],child)
   branch['child_to_extension']=row_witness(child['matrix'],extension)
 dag['certificate_version']='integer-lattice-inclusions-v1'
 (directory/f'{r}-{s}-certified.json').write_text(json.dumps(dag,default=int)+'\n')
 return len(dag['roots']),len(dag['nodes']),sum(len(n.get('branches',[])) for n in dag['nodes'])


def main():
 p=argparse.ArgumentParser();p.add_argument('--directory',type=Path,default=Path('results/2026-09-30-six-fibers'));a=p.parse_args()
 for profile in ((4,2),(3,3)):print(profile,certify(profile,a.directory),flush=True)
if __name__=='__main__':main()
