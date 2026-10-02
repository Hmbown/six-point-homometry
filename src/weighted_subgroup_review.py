"""Independent controls for coset and punctured-support phase ambiguities.

This auditor imports no author's weighted-subgroup implementation. Exact
fractions, symbolic polynomial identities and an independent ambient DFT
control are kept separate. Only small explicit supports are examined.
"""
from __future__ import annotations

import argparse
from fractions import Fraction as Q
import json
from math import gcd
from pathlib import Path

import numpy as np
import sympy as sp

ROOT = Path(__file__).resolve().parents[1]


def support(m: int):
    n=7*m
    return n,tuple(sorted(r+7*j for r in (0,1,3) for j in range(m)))


def support_q(q: int,m: int,quotient=(0,1,3)):
    return q*m,tuple(sorted(r+q*j for r in quotient for j in range(m)))


def periods(n: int, s):
    points=set(s)
    return tuple(h for h in range(n) if {(x+h)%n for x in s}==points)


def folded_differences(n: int, s):
    return tuple(sorted({min((a-b)%n,(b-a)%n) for a in s for b in s}))


def rational_kernel(t: Q):
    d=1+3*t*t
    return ((1-t*t)/d,2*t*(t-1)/d,2*t*(t+1)/d)


def convolve(x, u):
    n=len(x)
    return tuple(sum(u[j]*x[(i-j)%n] for j in range(n)) for i in range(n))


def autocorrelation(x):
    n=len(x)
    return tuple(sum(x[i]*x[(i+lag)%n] for i in range(n)) for lag in range(n))


def rigid_squared_distance(x,y):
    n=len(x)
    return min(sum((y[i]-sgn*x[(sgn_ref*i+shift)%n])**2 for i in range(n))
               for shift in range(n) for sgn_ref in (1,-1) for sgn in (1,-1))


def witness():
    n,s=support(3)
    x=[Q(0) for _ in range(n)]
    # Three independent coset blocks, with positive integer amplitudes.
    for r,block in [(0,(2,3,5)),(1,(7,11,13)),(3,(17,19,23))]:
        for j,v in enumerate(block):x[r+7*j]=Q(v)
    u=[Q(0) for _ in range(n)]
    for j,v in enumerate(rational_kernel(Q(1,6))):u[7*j]=v
    y=convolve(x,u)
    assert tuple(i for i,v in enumerate(y) if v)==s
    return n,s,tuple(x),tuple(u),y


def symbolic_kernel_identity():
    t=sp.symbols('t',real=True)
    numerator=(1-t*t,2*t*(t-1),2*t*(t+1))
    denominator=1+3*t*t
    identities=[sum(numerator)-denominator,
                sum(v*v for v in numerator)-denominator**2,
                sum(numerator[i]*numerator[(i+1)%3] for i in range(3))]
    assert all(sp.expand(v)==0 for v in identities)
    return [str(sp.expand(v)) for v in identities]


def exact_jacobian(n, s, x):
    # a_l(x) = sum_i x_i x_(i+l), so da_l/dx_s=x_(s+l)+x_(s-l).
    return sp.Matrix([[x[(j+lag)%n]+x[(j-lag)%n] for j in s]
                      for lag in range(n//2+1)])


def ambient_phase_control(m: int):
    n,s=support(m)
    h=tuple(range(0,n,7))
    phases=np.ones(m,dtype=np.complex128)
    for k in range(1,(m-1)//2+1):
        phases[k]=np.exp(1j*(0.09+0.013*k))
        phases[-k]=phases[k].conjugate()
    local=np.fft.ifft(phases)
    assert np.max(np.abs(local.imag))<1e-14
    u=np.zeros(n);u[list(h)]=local.real
    # Ambient characters restrict to H as k modulo m.
    fu=np.fft.fft(u)
    assert np.max(np.abs(fu-phases[np.arange(n)%m]))<2e-14
    x=np.zeros(n);x[list(s)]=np.arange(1,len(s)+1)/20+2
    y=np.fft.ifft(np.fft.fft(u)*np.fft.fft(x)).real
    outside=sorted(set(range(n))-set(s))
    outside_error=max(abs(y[i]) for i in outside)
    power_error=float(np.max(np.abs(np.abs(np.fft.fft(x))**2-np.abs(np.fft.fft(y))**2)))
    assert outside_error<2e-14 and min(y[list(s)])>0
    assert power_error<2e-10
    return {'n':n,'K':len(s),'periods':list(periods(n,s)),
            'folded_distances':list(folded_differences(n,s)),
            'torus_dimension':(m-1)//2,'ambient_dft_error':float(np.max(np.abs(fu-phases[np.arange(n)%m]))),
            'outside_support_error':float(outside_error),'minimum_amplitude':float(min(y[list(s)])),
            'power_error':power_error}


def exact_rank_control(q: int,m: int,quotient=(0,1,3)):
    n,s=support_q(q,m,quotient)
    ordered=[(r-t)%q for r in quotient for t in quotient if r!=t]
    assert len(set(ordered))==len(quotient)*(len(quotient)-1)
    x=[Q(0) for _ in range(n)]
    for r in quotient:
        for j in range(m):x[r+q*j]=Q(5+3*r+j)
    J=exact_jacobian(n,s,x)
    columns=[]
    for j in range(1,(m-1)//2+1):
        a=[Q(0) for _ in range(n)]
        a[q*j]=1;a[q*(m-j)]=-1
        tangent=convolve(x,a)
        columns.append([tangent[i] for i in s])
    T=sp.Matrix.hstack(*(sp.Matrix(v) for v in columns))
    rank=J.rank();tangent_rank=T.rank()
    assert tangent_rank==(m-1)//2
    assert J*T==sp.zeros(n//2+1,(m-1)//2)
    assert rank==len(s)-(m-1)//2
    # A separate ambient frequency-block calculation reconstructs every
    # ordered pair product from inverse q-DFT of the measured powers.
    xf=np.fft.fft(np.array(x,dtype=float))
    maximum=0.
    for ell in range(m):
        coeff=np.zeros(q,dtype=np.complex128)
        for r in quotient:
            block=np.array([float(x[r+q*j]) for j in range(m)])
            coeff[r]=np.fft.fft(block)[ell]*np.exp(-2j*np.pi*ell*r/n)
        measured=xf[ell+m*np.arange(q)]
        maximum=max(maximum,float(np.max(np.abs(np.fft.fft(coeff)-measured))))
        products=np.fft.ifft(np.abs(measured)**2)
        for r in quotient:
            for t in quotient:
                if r!=t:
                    maximum=max(maximum,float(abs(products[(r-t)%q]-coeff[r]*coeff[t].conjugate())))
    assert maximum<1e-9
    expected=len(quotient)*(len(quotient)-1)*m//2+m//2+1
    assert len(folded_differences(n,s))==expected
    return {'q':q,'m':m,'quotient':list(quotient),'N':n,'K':len(s),
            'folded_difference_count':expected,'jacobian_rank':rank,
            'tangent_rank':tangent_rank,'frequency_block_error':maximum}


def punctured_rank_control(q: int,m: int):
    """Exact transverse rank after deleting coordinate zero from a coset lift."""
    n,full=support_q(q,m)
    s=tuple(i for i in full if i)
    x=[Q(0) for _ in range(n)]
    for r in (0,1,3):
        for j in range(m):x[r+q*j]=Q(5+3*r+j)
    x[0]=Q(0)
    z=sp.symbols('z')
    for r in (0,1,3):
        polynomial=sum(sp.Rational(x[r+q*j])*z**j for j in range(m))
        assert sp.gcd(polynomial,z**m-1)==1
    # Obtain the hole's differential independently by ambient convolution.
    columns=[]
    for j in range(1,(m-1)//2+1):
        skew=[Q(0) for _ in range(n)]
        skew[q*j]=1;skew[q*(m-j)]=-1
        columns.append(convolve(x,skew))
    hole_gradient=[column[0] for column in columns]
    assert hole_gradient[0]==m-2 and hole_gradient[0]!=0
    tangents=[sp.Matrix([hole_gradient[0]*columns[j][i]
                        -hole_gradient[j]*columns[0][i] for i in s])
              for j in range(1,len(columns))]
    T=sp.Matrix.hstack(*tangents)
    J=exact_jacobian(n,s,x)
    assert J*T==sp.zeros(n//2+1,len(tangents))
    assert T.rank()==(m-1)//2-1
    assert J.rank()==3*m-(m-1)//2
    assert periods(n,s)==(0,)
    assert folded_differences(n,s)==folded_differences(n,full)
    assert len(folded_differences(n,s))==7*m//2+1>len(s)
    assert len(s)<n/2
    return {'q':q,'m':m,'N':n,'K':len(s),'periods':[0],
            'folded_difference_count':len(folded_differences(n,s)),
            'hole_gradient':list(map(str,hole_gradient)),
            'jacobian_rank':J.rank(),'hole_tangent_rank':T.rank()}


def independent_puncture_certificate():
    """Reconstruct the author's Z35 algebraic witness without author imports."""
    q,m=7,5
    n,full=support_q(q,m)
    s=tuple(i for i in full if i)
    blocks={0:(0,2,3,5,7),1:(11,13,17,19,23),3:(29,31,37,41,43)}
    x=[0]*n
    for r,block in blocks.items():
        for j,value in enumerate(block):x[r+q*j]=value
    # Solve (I-A)w=x first, then Cx=2w-x. This avoids the author's
    # adjugate multiplication and independently obtains the hole numerator.
    t=sp.symbols('t',real=True)
    shift=sp.Matrix(m,m,lambda i,j:int((i-j)%m==1))
    l1=shift-shift.T;l2=shift**2-(shift**2).T
    skew=t*l1+sp.Rational(1,1000)*l2
    w=(sp.eye(m)-skew).inv()*sp.Matrix(blocks[0])
    hole=sp.cancel(2*w[0]-blocks[0][0])
    polynomial=sp.Poly(sp.fraction(hole)[0],t).primitive()[1]
    expected=[17000000000000,7966000000000,7982983000000,4998001034000,2009009017]
    assert polynomial.all_coeffs()==expected
    interval=(sp.Rational(-6,14917),sp.Rational(-5,12431))
    assert polynomial.count_roots(*interval)==1
    assert -sp.Rational(1,1000)<interval[0]<interval[1]<sp.Rational(1,1000)
    assert polynomial.eval(interval[0])*polynomial.eval(interval[1])<0
    norm2=sum(v*v for v in x)
    bound=sp.Rational(8,1000)**2*norm2
    minimum=min(sum((x[i]-sign*x[(orientation*i+offset)%n])**2 for i in range(n))
                for sign in (-1,1) for orientation in (-1,1) for offset in range(n)
                if (sign,orientation,offset)!=(1,1,0))
    assert norm2==8257 and bound<1 and minimum==502
    derivative=2*(-sp.Rational(2,5)*l1+l2)
    ambient=[0]*n
    for r,block in blocks.items():
        for j,value in enumerate(derivative*sp.Matrix(block)):ambient[r+q*j]=value
    assert ambient[0]==0 and any(ambient)
    J=exact_jacobian(n,s,x)
    assert J.rank()==13 and J*sp.Matrix([ambient[i] for i in s])==sp.zeros(18,1)
    return {'N':n,'quartic_coefficients':list(map(str,polynomial.all_coeffs())),
            'isolating_interval':list(map(str,interval)),'interval_root_count':1,
            'norm_squared_x':norm2,'strict_displacement_squared_bound':str(bound),
            'minimum_nonidentity_intrinsic_squared_separation':minimum,
            'jacobian_shape':[18,14],'jacobian_rank':13,
            'exact_hole_tangent':list(map(str,ambient))}


def stability_control(q: int,m: int):
    """Independent untwisted gauge and Parseval control, with nonzero anchor."""
    quotient=(3,0,1)
    n=q*m
    x=np.zeros(n);y=np.zeros(n)
    for r in quotient:
        for j in range(m):
            x[r+q*j]=2+0.17*r+0.11*j+0.013*j*j
            y[r+q*j]=x[r+q*j]+0.004*np.sin(0.7+j+2*r)
    blocks=[np.array([signal[r::q] for r in quotient]) for signal in (x,y)]
    transforms=[np.fft.fft(block,axis=1) for block in blocks]
    magnitudes=np.concatenate([abs(v).ravel() for v in transforms])
    delta=float(min(magnitudes));M=float(max(magnitudes))
    assert delta>0
    power=[abs(np.fft.fft(signal))**2 for signal in (x,y)]
    canonical=[]
    product_error=0.
    for powers,target in zip(power,transforms):
        recovered=np.zeros((3,m),dtype=np.complex128)
        for ell in range(m):
            products=np.fft.ifft(powers[ell+m*np.arange(q)])
            def product(a,b):
                return products[(a-b)%q]*np.exp(2j*np.pi*ell*(a-b)/n)
            a,b,c=quotient
            anchor=np.sqrt(abs(product(a,b))*abs(product(a,c))/abs(product(b,c)))
            recovered[0,ell]=anchor
            for index,r in enumerate(quotient[1:],1):
                recovered[index,ell]=product(r,a)/anchor
            for i,r in enumerate(quotient):
                for j,s in enumerate(quotient):
                    if i!=j:product_error=max(product_error,abs(product(r,s)-target[i,ell]*target[j,ell].conjugate()))
        expected=target*np.exp(-1j*np.angle(target[0]))
        assert np.max(abs(recovered-expected))<2e-10
        assert np.max(abs(np.fft.ifft(recovered,axis=1).imag))<2e-12
        canonical.append(recovered)
    L0=(2*M*M/(delta*delta)+M**4/delta**4)/(2*delta)
    L1=1/delta+M*M*L0/(delta*delta)
    L=max(L0,L1)
    power_error=float(np.linalg.norm(power[0]-power[1]))
    gauge_distance=float(np.linalg.norm(canonical[0]-canonical[1])/np.sqrt(m))
    lower_bound=float(np.sqrt(3/n)*L*power_error)
    assert gauge_distance<=lower_bound
    # Minimize common phases independently, keeping both members real.
    squared=sum(np.sum(abs(v)**2) for v in transforms)-2*np.sum(abs(np.sum(transforms[0]*transforms[1].conjugate(),axis=0)))
    orbit_distance=float(np.sqrt(max(0.,squared/m)))
    assert orbit_distance<=gauge_distance+2e-10
    R=max(np.linalg.norm(x),np.linalg.norm(y))
    assert power_error<=2*n*R*orbit_distance+2e-10
    return {'q':q,'m':m,'fixed_untwisted_anchor':3,
            'pairproduct_error':float(product_error),'delta':delta,'M':M,
            'orbit_distance':orbit_distance,'canonical_gauge_distance':gauge_distance,
            'power_error':power_error,'recovery_bound':lower_bound}


def audit():
    identities=symbolic_kernel_identity()
    n,s,x,u,y=witness()
    assert tuple(i for i,v in enumerate(x) if v)==tuple(i for i,v in enumerate(y) if v)==s
    assert all(y[i]>0 for i in s)
    au=autocorrelation(u)
    assert au==(Q(1),)+(Q(0),)*(n-1)
    assert autocorrelation(x)==autocorrelation(y)
    minimum=rigid_squared_distance(x,y)
    assert minimum>0
    derivative=[Q(0) for _ in range(n)]
    derivative[7]=-2;derivative[14]=2
    tangent=convolve(x,derivative)
    J=exact_jacobian(n,s,x)
    assert J.rank()==8 and J*sp.Matrix([tangent[i] for i in s])==sp.zeros(11,1)
    z=sp.symbols('z')
    p=sum(sp.Rational(v.numerator,v.denominator)*z**i for i,v in enumerate(x))
    spectral_gcd=sp.gcd(sp.Poly(p,z),sp.Poly(z**n-1,z))
    assert spectral_gcd.degree()==0
    return {'status':'COMPUTED','scope':'small exact independent controls, not a novelty claim',
            'symbolic_kernel_identities':identities,'N':n,'support':list(s),
            'folded_distances':list(folded_differences(n,s)),
            'x':[str(v) for v in x],'u':[str(v) for v in u],'y':[str(v) for v in y],
            'minimum_positive_y':str(min(y[i] for i in s)),
            'minimum_rigid_squared_distance':str(minimum),
            'jacobian_shape':[11,9],'jacobian_rank':J.rank(),
            'tangent':[str(v) for v in tangent],
            'spectral_polynomial_gcd':str(spectral_gcd.as_expr()),
            'general_family_controls':[ambient_phase_control(m) for m in range(3,13)],
            'exact_rank_controls':[exact_rank_control(q,m) for q in (7,8,9) for m in range(3,9)]
                                  +[exact_rank_control(13,m,(0,1,3,9)) for m in (3,4)],
            'punctured_rank_controls':[punctured_rank_control(q,m) for q in (7,8,9) for m in range(5,11)],
            'punctured_algebraic_certificate':independent_puncture_certificate(),
            'stability_controls':[stability_control(q,m) for q in (7,8,9) for m in range(3,10)]}


def main():
    p=argparse.ArgumentParser()
    p.add_argument('--out',type=Path,default=ROOT/'results/2026-10-01-weighted-subgroup-review/independent-audit.json')
    args=p.parse_args();result=audit()
    args.out.parent.mkdir(parents=True,exist_ok=True)
    args.out.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:result[k] for k in ('status','N','support','jacobian_rank','minimum_rigid_squared_distance')}))


if __name__=='__main__':main()
