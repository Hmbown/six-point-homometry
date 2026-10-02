"""Public certificate driver: finite paths, arbitrary moduli, exact replay."""
from __future__ import annotations
from collections import Counter
from copy import deepcopy
from itertools import combinations
from pathlib import Path
from random import Random
import json,sys,time
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'src'))
import six_generate as driver
from homometry import icv,dihedral_canon
from six_shell import parametric_families
from test_six_pair_mechanisms import check as independent_saved_check


def main():
 start=time.monotonic();out=ROOT/'results/2026-09-30-six-generate';out.mkdir(exist_ok=True);rng=Random(602135);checks=0
 # Independent agreement with the immutable reference, including even n
 # antipodes and nonzero input translations/inversions.
 for n in range(6,61):
  for trial in range(12):
   a=tuple(sorted(rng.sample(range(n),6)));v=icv(a,n)
   assert driver.canon(a,n)==dihedral_canon(a,n)
   assert driver.interval_counter(a,n)==Counter({d+1:k for d,k in enumerate(v) if k});checks+=1
 # Every historically missing direct edge is recovered as an actual saved
 # finite-family path. Verify each embedded edge by the independent old
 # replay checker as well, retaining its original parity/seed semantics.
 saved=json.loads((ROOT/'results/2026-09-30-six-finite-torsion-review.json').read_text());paths=[];edge_labels=Counter()
 for old in saved['missing_edge_paths']:
  n=old['n'];a,b=old['vertices'][0],old['vertices'][-1]
  cert=driver.generate(n,a,b,prefer_finite=True);assert cert['route']=='finite_path' and len(cert['path']['edges'])>=2
  assert driver.replay(json.loads(json.dumps(cert)))==list(map(tuple,cert['vertices']))
  for edge in cert['path']['edges']:independent_saved_check(edge,cert['path']['modulus']);edge_labels[edge['label']]+=1
  paths.append(cert)
 assert len(paths)==73
 (out/'all-73-finite-paths.json').write_text(json.dumps(paths)+'\n')
 # Every legacy schema, including unit and rigid seed certificates, remains
 # executable rather than being silently relabelled as a new mechanism.
 representatives={}
 for n in range(12,136):
  report=json.loads((ROOT/f'results/2026-09-30-six-pair-mechanisms/n{n}.json').read_text())
  for c in report['certificates']:
   if c['label'] not in representatives:representatives[c['label']]=(n,c)
  if len(representatives)==9:break
 for n,c in representatives.values():driver.verify_saved(c,n);independent_saved_check(c,n)
 assert len(representatives)==9
 # Genuine arbitrary-size positive-rank examples, including a prime far
 # beyond any census and three proven integer-nonshadow order-six families.
 cases=[]
 def save_case(name,n,a,b,finite=False):
  cert=driver.generate(n,a,b,prefer_finite=finite);assert cert['a']!=cert['b'];assert driver.replay(cert)==cert['vertices']
  (out/f'{name}.json').write_text(json.dumps(cert,indent=2)+'\n');cases.append({'name':name,'n':n,'route':cert['route'],'label':cert.get('certificate',{}).get('label') if cert.get('certificate') else None,'support':cert['ordinary_support']});return cert
 save_case('HR22-inflated',22*10007,[10007*x+19 for x in (0,1,3,6,13,17)],[-10007*x+71 for x in (0,1,3,8,13,19)])
 save_case('Bloom-large-prime',1000000007,(0,1,4,10,12,17),(0,1,8,11,13,17))
 for index,(a,b) in enumerate(parametric_families(1000003,101),1):save_case(f'nonshadow-H{index}',6000018,a,b)
 l3=save_case('generalized-L3-large',3000090,(0,147789,600018,800024,1347825,1747837),(0,147789,547801,1747837,2200066,2400072));assert l3['certificate']['label']=='L3*'
 # L7's target is disjoint from A, so its discovery must align B to the
 # complement itself, not reuse the nonempty-intersection block alignments.
 m=100003;n=4*m;a=(0,m,1,1+2*m,3,3+2*m);b=(2*m,3*m,1+m,1+3*m,3+m,3+3*m)
 assert set(a).isdisjoint(b)
 pure=driver.halfcoset_certificate(a,b,n);assert pure and pure['label']=='L7'
 driver.verify_direct(a,b,n,pure)
 l7=save_case('L7-disjoint-complement-large',n,a,b);assert l7['certificate']['label']=='L7'
 small=driver.generate(16,(0,1,3,4,9,11),(0,1,3,9,11,12));assert small['certificate']['label']=='L7'
 # An ordinary-inflated missing edge uses source certificates unchanged.
 old=saved['missing_edge_paths'][0];n=old['n']*100003
 large=save_case('missing-edge-inflated',n,[100003*x+3 for x in old['vertices'][0]],[-100003*x+17 for x in old['vertices'][-1]],True)
 assert len(large['path']['edges'])>=2
 # Replay is portable: the source table is not needed after generation.
 original_graph=driver.finite_graph
 driver.finite_graph=lambda q:(_ for _ in ()).throw(AssertionError('replay accessed finite table'))
 try:assert driver.replay(large)==large['vertices']
 finally:driver.finite_graph=original_graph
 # Odd modular move in even n: no half-shift exists. The generalized L3*
 # identity still verifies exactly, and this pair is genuinely non-T/I.
 odd={'label':'L3*','b_sign':1,'b_shift':9,'fixed':[1,7],'move':9};a=(0,1,3,5,7,8);b=(0,3,4,5,8,10)
 assert dihedral_canon(a,12)!=dihedral_canon(b,12) and icv(a,12)==icv(b,12)
 assert all(2*t%12!=9 for t in range(12));driver.verify_direct(a,b,12,odd)
 (out/'odd-halfshift-L3star.json').write_text(json.dumps({'n':12,'a':a,'b':b,'certificate':odd},indent=2)+'\n')
 # Negative and tamper controls, plus trivial homometry handled honestly.
 for n,a,b in ((17,(0,1,2,3,4,5),(0,1,2,3,4,6)),(12,(0,1,1,3,5,6),(0,1,2,3,5,6))):
  try:driver.generate(n,a,b)
  except ValueError:pass
  else:raise AssertionError('invalid input accepted')
 trivial=driver.generate(31,(0,1,3,7,10,15),(8,9,11,15,18,23));assert trivial['route']=='TI'
 bad=deepcopy(large);bad['path']['edges'][0]['a'][1]+=1
 try:driver.replay(bad)
 except (ValueError,AssertionError):pass
 else:raise AssertionError('tampered edge accepted')
 bad=deepcopy(large);bad['vertices'][0]=tuple((x+1)%bad['n'] for x in bad['vertices'][0])
 try:driver.replay(bad)
 except ValueError:pass
 else:raise AssertionError('false advertised path accepted')
 bad=deepcopy(large);bad['n']=float(bad['n'])
 try:driver.replay(bad)
 except ValueError:pass
 else:raise AssertionError('floating certificate arithmetic accepted')
 bad=deepcopy(odd);bad['move']=8
 try:driver.verify_direct(a=(0,1,3,5,7,8),b=(0,3,4,5,8,10),n=12,c=bad)
 except ValueError:pass
 else:raise AssertionError('tampered L3* accepted')
 # An implementation coverage failure is an invariant error, not a false
 # decision that the input is nonhomometric.
 original_direct=driver.direct_certificate;driver.direct_certificate=lambda *args:None
 try:
  try:driver.generate(1000000007,(0,1,4,10,12,17),(0,1,8,11,13,17))
  except driver.GenerationInvariantError:pass
  else:raise AssertionError('missing direct implementation was not reported')
 finally:driver.direct_certificate=original_direct
 result={'status':'COMPUTED public generator/replay checks passed','reference_random_sets':checks,'missing_direct_pairs_recovered':len(paths),'saved_path_edge_labels':dict(edge_labels),'legacy_schema_labels':sorted(representatives),'large_cases':cases,'odd_halfshift_L3star':True,'disjoint_L7_discovery':True,'advertised_path_tamper_rejected':True,'seconds':time.monotonic()-start}
 (out/'verification.json').write_text(json.dumps(result,indent=2)+'\n');print(result,flush=True)
if __name__=='__main__':main()
