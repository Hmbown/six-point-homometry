"""Checkpointed exhaustive cross-orbit/quotient-DAG builder for all low-rank strata."""
import argparse,gzip,json,time
from pathlib import Path
from six_free_dag import cross_orbits,search,ROOT


def main():
    p=argparse.ArgumentParser();p.add_argument('--out',type=Path,default=ROOT/'results/2026-09-30-six-free-dag-all')
    p.add_argument('--max-nodes',type=int,default=10000);p.add_argument('--resume',action='store_true');a=p.parse_args();a.out.mkdir(parents=True,exist_ok=True)
    rows=[];start=time.monotonic()
    for rank in (3,4):
        strata=json.loads((ROOT/f'results/2026-09-30-six-free-rank/rank{rank}-orbits.json').read_text())['orbits']
        for orbit in strata:
            stem=f'rank{rank}-orbit{orbit["index"]:03}';target=a.out/f'{stem}.json.gz';crosspath=a.out/f'{stem}-cross.json.gz'
            if a.resume and target.exists() and crosspath.exists():
                with gzip.open(target,'rt') as handle:result=json.load(handle)
                with gzip.open(crosspath,'rt') as handle:cross=json.load(handle)
            else:
                cross=cross_orbits(orbit['heights'])
                with gzip.open(crosspath,'wt') as handle:json.dump(cross,handle,default=int);handle.write('\n')
                result=search(orbit['heights'],a.max_nodes,root_matrices=cross['records'])
                result.update(orbit=orbit,height_rank=rank)
                with gzip.open(target,'wt') as handle:json.dump(result,handle,default=int);handle.write('\n')
            unknown=[node['id'] for node in result['nodes'] if node.get('terminal')=='homometric' and not node.get('block')]
            row=dict(rank=rank,orbit=orbit['index'],complete=result['complete'],cross_bijections=cross['covered'],cross_orbits=cross['orbits'],
                     nodes=len(result['nodes']),terminal_histogram=result['terminal_histogram'],unrecognized=unknown,seconds=result['seconds'])
            rows.append(row)
            (a.out/'summary.json').write_text(json.dumps(dict(status='COMPUTED-UNVALIDATED pending exhaustive independent audit',strata=rows,seconds=time.monotonic()-start),indent=2)+'\n')
            print(row,'elapsed',round(time.monotonic()-start,2),flush=True)
    print('DONE',len(rows),'incomplete',[(r['rank'],r['orbit']) for r in rows if not r['complete']],
          'unrecognized',sum(len(r['unrecognized']) for r in rows),flush=True)

if __name__=='__main__':main()
