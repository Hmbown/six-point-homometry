/-
Soundness of the generating moves of Theorem G, as identities in the
integral group ring ℤ[G] of an arbitrary additive commutative group G.

Each move of the six-point grammar is sound because of a short identity
in ℤ[G] that holds for *arbitrary* ring elements (indicator functions are
a special case, and disjointness of the blocks is only needed to know that
the sum of two indicators is again an indicator).  These are the
identities stated in Section 2 of `notes/2026-09-30-six-generation.md`.

Author: Hunter Bown, with AI assistance.  Checked against Mathlib
(see `formal/README.md` for the exact commit).
-/
import Mathlib.Algebra.MonoidAlgebra.Basic
import Mathlib.Tactic.LinearCombination
import Mathlib.Tactic.Ring

namespace SixPointHomometry

open AddMonoidAlgebra

variable {G : Type*} [AddCommGroup G]

/-- The group ring `ℤ[G]`. -/
abbrev R (G : Type*) [AddCommGroup G] := AddMonoidAlgebra ℤ G

/-- The reflection `F ↦ F*`, sending `x^g` to `x^{-g}`.  It is a ring
automorphism of `ℤ[G]` because `g ↦ -g` is an additive automorphism. -/
noncomputable def star' : R G ≃ₐ[ℤ] R G :=
  AddMonoidAlgebra.domCongr ℤ ℤ (AddEquiv.neg G)

/-- The monomial `x^g`. -/
noncomputable def x (g : G) : R G := single g 1

/-- The autocorrelation `F F*`. -/
noncomputable def ac (F : R G) : R G := F * star' F

lemma star'_x (g : G) : star' (x g : R G) = x (-g) := by
  simp [star', x, AddMonoidAlgebra.domCongr_single]

lemma star'_mul (F H : R G) : star' (F * H) = star' F * star' H := map_mul _ _ _
lemma star'_add (F H : R G) : star' (F + H) = star' F + star' H := map_add _ _ _
lemma star'_sub (F H : R G) : star' (F - H) = star' F - star' H := map_sub _ _ _
lemma star'_one : star' (1 : R G) = 1 := map_one _

lemma star'_star' (F : R G) : star' (star' F) = F := by
  ext n
  simp [star', AddMonoidAlgebra.domCongr_apply]

lemma x_mul_x (g h : G) : (x g : R G) * x h = x (g + h) := by
  simp [x, single_mul_single]

lemma x_zero : (x (0 : G) : R G) = 1 := rfl

lemma x_mul_x_neg (g : G) : (x g : R G) * x (-g) = 1 := by
  rw [x_mul_x, add_neg_cancel, x_zero]

/-! ### Block translations and reflection

Throughout, `A = U + W` is the set written as a disjoint sum of a fixed
block `U` and a moving block `W`, and `P = U W*` is the cross term, so that
`A A* = U U* + W W* + P + P*`. -/

/-- **L2 (periodic translation).** If `x^s P = P`, moving the block `W` by
`s` preserves the autocorrelation. -/
theorem L2 (U W : R G) (s : G) (h : x s * (U * star' W) = U * star' W) :
    ac (U + x s * W) = ac (U + W) := by
  have hx := x_mul_x_neg (G := G) s
  have hinv : x (-s) * (U * star' W) = U * star' W := by
    calc x (-s) * (U * star' W) = x (-s) * (x s * (U * star' W)) := by rw [h]
      _ = (x s * x (-s)) * (U * star' W) := by ring
      _ = U * star' W := by rw [hx, one_mul]
  have hstar : x s * (star' U * W) = star' U * W := by
    have := congrArg star' hinv
    simpa only [star'_mul, star'_x, neg_neg, star'_star'] using this
  simp only [ac, star'_add, star'_mul, star'_x]
  linear_combination hinv + hstar + (W * star' W) * hx

/-- **L3\* (cosymmetric translation).** If `x^{-s} P = P*`, moving `W` by
`s` exchanges the two cross terms and preserves the autocorrelation. -/
theorem L3star (U W : R G) (s : G)
    (h : x (-s) * (U * star' W) = star' U * W) :
    ac (U + x s * W) = ac (U + W) := by
  have hx := x_mul_x_neg (G := G) s
  have h' : x s * (star' U * W) = U * star' W := by
    have := congrArg star' h
    simpa only [star'_mul, star'_x, neg_neg, star'_star'] using this
  simp only [ac, star'_add, star'_mul, star'_x]
  linear_combination h + h' + (W * star' W) * hx

/-- **L4 (half-turn translation).** If `2s = 0` and `x^s (P + P*) = P + P*`,
moving `W` by `s` preserves the autocorrelation. -/
theorem L4 (U W : R G) (s : G) (hs : s + s = 0)
    (h : x s * (U * star' W + star' U * W) = U * star' W + star' U * W) :
    ac (U + x s * W) = ac (U + W) := by
  have hneg : (-s : G) = s := neg_eq_of_add_eq_zero_left hs
  have hss : (x s : R G) * x s = 1 := by
    have := x_mul_x_neg (G := G) s
    rwa [hneg] at this
  simp only [ac, star'_add, star'_mul, star'_x, hneg]
  linear_combination h + (W * star' W) * hss

/-- **L5 (block reflection).** If `U W* = x^{-c} U W`, replacing `W` by its
reflection `x^c W*` preserves the autocorrelation. -/
theorem L5 (U W : R G) (c : G) (h : U * star' W = x (-c) * (U * W)) :
    ac (U + x c * star' W) = ac (U + W) := by
  have hx := x_mul_x_neg (G := G) c
  have h' : star' U * W = x c * (star' U * star' W) := by
    have := congrArg star' h
    simpa only [star'_mul, star'_x, neg_neg, star'_star'] using this
  simp only [ac, star'_add, star'_mul, star'_x, star'_star']
  linear_combination -h - h' + (W * star' W) * hx

/-! ### Half-per-coset complementation -/

/-- **L7 (half-per-coset complementation), algebraic form.**  Let `J` be the
indicator of a finite subgroup `H` of even order `2k`, so `J* = J` and
`J J = 2k · J`.  Let `S = J C` be the union of the occupied cosets (`C` a
sum of coset representatives), and suppose `A` has exactly `k` points in
each occupied coset, which is the identity `J A = k · J C`.  Then the
complement `S - A` has the same autocorrelation as `A`. -/
theorem L7 (J C A : R G) (k : ℕ)
    (hJ : star' J = J)
    (hJJ : J * J = (2 * (k : R G)) * J)
    (hA : J * A = (k : R G) * (J * C)) :
    ac (J * C - A) = ac A := by
  have hA' : J * star' A = (k : R G) * (J * star' C) := by
    have := congrArg star' hA
    simpa only [star'_mul, hJ, map_natCast] using this
  simp only [ac, star'_sub, star'_mul, hJ]
  linear_combination (C * star' C) * hJJ - C * hA' - (star' C) * hA

/-! ### The parallelogram-dyad identity -/

/-- **D (dyad exchange), the exact identity.**  For arbitrary `C` and
`a, b`, with `X = C + 1 + x^{a+b}` and `Y = C + x^a + x^b`,
`X X* - Y Y* = x^{-a-b} (1 - x^a)(1 - x^b) · K` where
`K = C + x^{a+b} C* + (1 + x^a)(1 + x^b)`. -/
theorem D_identity (C : R G) (a b : G) :
    ac (C + 1 + x (a + b)) - ac (C + x a + x b)
      = x (-(a + b)) * (1 - x a) * (1 - x b)
          * (C + x (a + b) * star' C + (1 + x a) * (1 + x b)) := by
  have hu := x_mul_x_neg (G := G) a
  have hv := x_mul_x_neg (G := G) b
  have hab : (x (a + b) : R G) = x a * x b := by rw [x_mul_x]
  have hab' : (x (-(a + b)) : R G) = x (-a) * x (-b) := by rw [x_mul_x, neg_add]
  simp only [ac, star'_add, star'_x, star'_one]
  rw [hab, hab']
  linear_combination
    (-(C * x (-b) * x b) + C * x (-b) - star' C * x (-b) * x a * x b * x b
      + star' C * x (-b) * x a * x b + star' C * x (-b) * x b * x b - star' C * x (-b) * x b
      - x (-b) * x a * x b * x b + x (-b) * x a + x (-b) * x b - 1) * hu
    + (C * x (-a) - C - star' C * x a * x b + star' C * x a + star' C * x b - star' C
      + x (-a) * x b - x a * x b) * hv

/-- **D (dyad exchange), soundness.**  If the kernel `K` is annihilated by
`(1 - x^a)(1 - x^b)`, the exchange preserves the autocorrelation. -/
theorem D_sound (C : R G) (a b : G)
    (hK : (1 - x a) * (1 - x b) * (C + x (a + b) * star' C + (1 + x a) * (1 + x b)) = 0) :
    ac (C + 1 + x (a + b)) = ac (C + x a + x b) := by
  have h := D_identity C a b
  have h2 : ac (C + 1 + x (a + b)) - ac (C + x a + x b) = 0 := by
    rw [h]; linear_combination (x (-(a + b))) * hK
  exact sub_eq_zero.mp h2

end SixPointHomometry
