"""Functional regressions for exact formal-group mechanisms and DAG helpers.

The exhaustive independent audit is test_six_low_rank_mechanisms_review.py;
these small tests specifically exercise builder behavior and torsion handling.
"""
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'src'))
from sympy import Matrix
from six_free_mechanisms import classify,cyclic_quotients,autocorrelation
from six_free_dag import cross_orbits,search
from six_free_dag_certify import equivalence
from six_fibers import group_record


def main():
    # The formal two-parameter Bloom identity (no coordinate or modulus bound).
    a=((0,0),(1,0),(-2,1),(-2,2),(0,2),(-1,3))
    b=((0,0),(1,0),(2,1),(-1,2),(1,2),(-1,3))
    assert classify(a,b,(0,0))['label']=='Bloom'
    assert autocorrelation(a,(0,0))==autocorrelation(b,(0,0))
    # Reviewed rank-three antipodal master, with independent free generators.
    common=((0,0,0,0),(0,1,0,0),(0,0,1,0),(1,1,-1,0))
    a=common+((0,0,0,1),(1,0,0,1))
    b=common+((0,1,0,-1),(1,1,0,-1))
    assert classify(a,b,(2,0,0,0))['label']=='cosymmetric_translate'
    # Torsion characters must use the ACTUAL image, not the ambient exponent.
    chars=list(cyclic_quotients(a,b,(2,),3))
    assert len(chars)==2 and {c['image_order'] for c in chars}=={1,2}
    assert chars[0]['certificate']['label']=='collision'
    assert chars[1]['certificate']['label']!='template'
    # Generic heights have one cross matching and force labelled equality.
    heights=(0,1,3,7,15,31)
    cross=cross_orbits(heights)
    assert cross['covered']==cross['orbits']==1
    dag=search(heights,root_matrices=cross['records'])
    assert dag['complete'] and dag['terminal_histogram']=={'ti':1}
    # A non-saturated row lattice must never be replaced by its rational span.
    matrix=Matrix([[2]+[0]*9])
    record=group_record(matrix)
    cert=equivalence(matrix,record)
    assert Matrix(cert['to_canonical'])*matrix==matrix
    assert Matrix(cert['from_canonical'])*matrix==matrix
    try:equivalence(Matrix([[1]+[0]*9]),record)
    except AssertionError:pass
    else:raise AssertionError('non-saturated lattice was silently saturated')
    print('six_free_mechanisms: formal identities, actual-image characters, generic DAG, and integral-lattice regression passed')

if __name__=='__main__':main()
