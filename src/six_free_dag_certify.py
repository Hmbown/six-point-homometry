"""Attach exact two-way row-lattice witnesses to every saved DAG normalization."""
import argparse,gzip,json,time
from pathlib import Path
from sympy import Matrix,ZZ
from sympy.polys.matrices import DomainMatrix
from sympy.polys.matrices.normalforms import smith_normal_decomp
from six_free_dag import ROOT,edge_row


def integer_matrix(rows,cols=10):return Matrix(rows) if rows else Matrix.zeros(0,cols)
def row_coefficients(rows,u,v,diagonal):
    """Coefficients C with C*M=rows, using U*M*V=D; verify by multiplication elsewhere."""
    transformed=rows*v;coeff=Matrix.zeros(rows.rows,u.rows)
    for i in range(rows.rows):
        for j in range(10):
            value=int(transformed[i,j]);divisor=diagonal[j] if j<len(diagonal) else 0
            if divisor:
                assert value%divisor==0;coeff[i,j]=value//divisor
            else:assert value==0
    return coeff*u

def equivalence(source,child):
    target=integer_matrix(child['matrix']);cu=Matrix(child['smith_u']);cv=Matrix(child['smith_v']);cd=child['smith_diagonal']
    dd,uu,vv=smith_normal_decomp(DomainMatrix.from_Matrix(source).convert_to(ZZ))
    d,u,v=(m.to_Matrix() for m in (dd,uu,vv));diag=[int(d[i,i]) for i in range(min(d.shape))]
    forward=row_coefficients(target,u,v,diag);reverse=row_coefficients(source,cu,cv,cd)
    assert forward*source==target and reverse*target==source
    return dict(to_canonical=[[int(x) for x in row] for row in forward.tolist()],
                from_canonical=[[int(x) for x in row] for row in reverse.tolist()])


def main():
    p=argparse.ArgumentParser();p.add_argument('--base',type=Path,default=ROOT/'results/2026-09-30-six-free-dag-all');p.add_argument('--resume',action='store_true');a=p.parse_args()
    summary=json.loads((a.base/'summary.json').read_text());start=time.monotonic();counts={'roots':0,'branches':0};done=[]
    for row in summary['strata']:
        stem=f'rank{row["rank"]}-orbit{row["orbit"]:03}';target=a.base/f'{stem}.json.gz'
        with gzip.open(target,'rt') as handle:data=json.load(handle)
        if a.resume and data.get('normalizations_certified'):
            counts['roots']+=len(data['roots']);counts['branches']+=sum(len(n.get('branches',[])) for n in data['nodes']);done.append(stem);continue
        with gzip.open(a.base/f'{stem}-cross.json.gz','rt') as handle:cross=json.load(handle)
        records={r['id']:r for r in cross['records']}
        for root in data['roots']:
            source=integer_matrix(records[root['orbit_id']]['matrix']);child=data['nodes'][root['node']]
            root['row_lattice']=equivalence(source,child);counts['roots']+=1
        for node in data['nodes']:
            if not node.get('branches'):continue
            parent=integer_matrix(node['matrix']);ar=edge_row(node['chosen_a'],0)
            for branch in node['branches']:
                br=edge_row(branch['b_edge'],1);relation=[x-branch['sign']*y for x,y in zip(ar,br)]
                source=parent.col_join(Matrix([relation]));child=data['nodes'][branch['child']]
                branch['row_lattice']=equivalence(source,child);counts['branches']+=1
        data['normalizations_certified']=True
        temp=target.with_suffix('.tmp.gz')
        with gzip.open(temp,'wt') as handle:json.dump(data,handle,default=int);handle.write('\n')
        temp.replace(target);done.append(stem)
        print(stem,dict(counts),'seconds',round(time.monotonic()-start,2),flush=True)
    result=dict(complete=len(done)==len(summary['strata']),strata=len(done),**counts,seconds=time.monotonic()-start)
    (a.base/'normalizations.json').write_text(json.dumps(result,indent=2)+'\n');print(result,flush=True)

if __name__=='__main__':main()
