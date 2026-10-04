/-
The classical two-parameter six-point construction (Bloom; Yovanof–Golomb
"Family N") is sound: `X X* = Y Y*` in ℤ[G] for every additive commutative
group `G` and all `a, b : G`.  The proof is the signed factorization
`X = F·Q`, `Y = F·x^{2b-a}·Q*` with `F = 1 + x^a + x^b` and
`Q = 1 + x^{b-2a} - x^{b-a} + x^{2b-a}`.

Author: Hunter Bown, with AI assistance.
-/
import SixPointHomometry.Soundness
import Mathlib.Tactic.Abel

namespace SixPointHomometry

open AddMonoidAlgebra

variable {G : Type*} [AddCommGroup G]

/-- `X = {0, a, b-2a, 2b-2a, 2b, 3b-a}` as a group-ring element. -/
noncomputable def bloomX (a b : G) : R G :=
  1 + x a + x (b - (a + a)) + x (b + b - (a + a)) + x (b + b) + x (b + b + b - a)

/-- `Y = {0, a, 2a+b, 2b-a, a+2b, 3b-a}` as a group-ring element. -/
noncomputable def bloomY (a b : G) : R G :=
  1 + x a + x (a + a + b) + x (b + b - a) + x (a + b + b) + x (b + b + b - a)

noncomputable def bloomF (a b : G) : R G := 1 + x a + x b
noncomputable def bloomQ (a b : G) : R G := 1 + x (b - (a + a)) - x (b - a) + x (b + b - a)

lemma bloomX_eq (a b : G) : bloomX a b = bloomF a b * bloomQ a b := by
  have e1 : a + (b - (a + a)) = b - a := by abel
  have e2 : a + (b - a) = b := by abel
  have e3 : a + (b + b - a) = b + b := by abel
  have e4 : b + (b - (a + a)) = b + b - (a + a) := by abel
  have e5 : b + (b - a) = b + b - a := by abel
  have e6 : b + (b + b - a) = b + b + b - a := by abel
  simp only [bloomX, bloomF, bloomQ, add_mul, mul_add, mul_sub, one_mul, mul_one,
    x_mul_x, e1, e2, e3, e4, e5, e6]
  abel

lemma bloomY_eq (a b : G) : bloomY a b = bloomF a b * (x (b + b - a) * star' (bloomQ a b)) := by
  have hQ : x (b + b - a) * star' (bloomQ a b) = 1 + x (a + b) - x b + x (b + b - a) := by
    simp only [bloomQ, star'_add, star'_sub, star'_one, star'_x, mul_add, mul_sub, mul_one, x_mul_x]
    have e1 : b + b - a + -(b - (a + a)) = a + b := by abel
    have e2 : b + b - a + -(b - a) = b := by abel
    have e3 : b + b - a + -(b + b - a) = 0 := by abel
    rw [e1, e2, e3, x_zero]; abel
  rw [hQ]
  have e1 : a + (a + b) = a + a + b := by abel
  have e2 : a + (b + b - a) = b + b := by abel
  have e3 : b + (a + b) = a + b + b := by abel
  have e4 : b + (b + b - a) = b + b + b - a := by abel
  simp only [bloomY, bloomF, add_mul, mul_add, mul_sub, one_mul, mul_one, x_mul_x,
    e1, e2, e3, e4]
  abel

/-- **B (Bloom construction) is sound.** -/
theorem Bloom (a b : G) : ac (bloomX a b) = ac (bloomY a b) := by
  rw [bloomX_eq, bloomY_eq]
  simp only [ac, star'_mul, star'_x, star'_star']
  have hx := x_mul_x_neg (G := G) (b + b - a)
  linear_combination (bloomF a b * star' (bloomF a b) * bloomQ a b * star' (bloomQ a b)) * (-hx)

end SixPointHomometry
