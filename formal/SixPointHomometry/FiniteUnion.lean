/-
A vector space over an infinite field is not a finite union of proper
subspaces.  This is the step in Section 3.3 of the synthesis note that
fixes one congruence alignment for every real solution.  The hard work is
Mathlib's `Submodule.iUnion_ssubset_of_forall_ne_top_of_card_lt`; here we
state the two forms used in the proof.

Author: Hunter Bown, with AI assistance.
-/
import Mathlib.Algebra.Module.Submodule.Union
import Mathlib.SetTheory.Cardinal.Finite

namespace SixPointHomometry

variable {ι K M : Type*} [Field K] [Infinite K] [AddCommGroup M] [Module K M]

/-- Finitely many proper subspaces of a vector space over an infinite field
do not cover it. -/
theorem iUnion_ne_univ_of_forall_ne_top (s : Finset ι) (p : ι → Submodule K M)
    (h : ∀ i, p i ≠ ⊤) : (⋃ i ∈ s, (p i : Set M)) ≠ Set.univ := by
  have hcard : (s.card : ℕ∞) < ENat.card K := by
    rw [ENat.card_eq_top_of_infinite]; exact ENat.coe_lt_top _
  exact (Submodule.iUnion_ssubset_of_forall_ne_top_of_card_lt s p h hcard).ne

/-- If finitely many subspaces cover a vector space over an infinite field,
one of them is the whole space.  (Used with `K = ℝ` and the finitely many
congruence-alignment subspaces of `Hom(G_M, ℝ)`.) -/
theorem exists_eq_top_of_iUnion_eq_univ [DecidableEq ι] (s : Finset ι)
    (p : ι → Submodule K M) (hcover : (⋃ i ∈ s, (p i : Set M)) = Set.univ) :
    ∃ i ∈ s, p i = ⊤ := by
  by_contra hne
  push Not at hne
  have hs : s.Nonempty := by
    by_contra hemp
    rw [Finset.not_nonempty_iff_eq_empty] at hemp
    subst hemp
    have h0 : (0 : M) ∈ (⋃ i ∈ (∅ : Finset ι), (p i : Set M)) := hcover ▸ Set.mem_univ 0
    simp at h0
  obtain ⟨j₀, hj₀⟩ := hs
  let q : ι → Submodule K M := fun i => if i ∈ s then p i else p j₀
  have hq : ∀ i, q i ≠ ⊤ := by
    intro i
    by_cases hi : i ∈ s
    · simpa [q, hi] using hne i hi
    · simpa [q, hi] using hne j₀ hj₀
  have hcov' : (⋃ i ∈ s, (q i : Set M)) = Set.univ := by
    rw [← hcover]
    apply Set.iUnion₂_congr
    intro i hi
    simp [q, hi]
  exact iUnion_ne_univ_of_forall_ne_top s q hq hcov'

end SixPointHomometry
