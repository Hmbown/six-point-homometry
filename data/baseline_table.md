# Baseline census (reference, do not edit)

Method: all T_n/I classes of k-subsets, 2 ≤ k ≤ n−2, grouped by interval-class vector.
"Unexplained" = not connected by Babbitt complement / 0/1 direct-sum flip / flip-of-complements.

| n | Z-families | max family | by cardinality | unexplained | 3-deck families | source |
|---|---|---|---|---|---|---|
| 8 | 1 | 2 | {4:1} | 0 | 0 | census.py |
| 9 | 0 | 0 | {} | 0 | 0 | census.py |
| 10 | 3 | 2 | {5:3} | 0 | 0 | census.py |
| 11 | 0 | 0 | {} | 0 | 0 | census.py |
| 12 | 23 | 2 | {4:1,5:3,6:15,7:3,8:1} | 8 | 0 | census.py |
| 13 | 6 | 2 | {4:1,6:2,7:2,9:1} | 4 | 0 | census.py |
| 14 | 72 | 2 | {5:6,6:6,7:48,8:6,9:6} | 18 | 0 | census.py |
| 15 | 80 | 2 | {5:5,6:25,7:10,8:10,9:25,10:5} | 66 | 0 | census.py |
| 16 | 354 | 4 | {4:2,5:10,6:31,7:44,8:180,9:44,10:31,11:10,12:2} | 159 | 0 | census.py |
| 17 | 184 | 2 | – | – | 0 | earlier script (UNVALIDATED) / 3-deck via homometry.py |
| 18 | 1292 | 4 | – | – | 0 | earlier script (UNVALIDATED) / 3-deck via homometry.py |
| 19 | 648 | 2 | – | – | – | earlier script (UNVALIDATED) |
| 20 | 4932 | 6 | – | – | – | earlier script (UNVALIDATED) |

The 8 unexplained Z₁₂ families:
{0,1,3,7}/{0,1,4,6} · {0,1,2,4,7}/{0,1,3,5,6} · {0,1,2,5,8}/{0,1,3,8,9} · {0,1,2,5,9}/{0,1,3,4,8} ·
{0,1,2,3,4,7,9}/{0,1,2,3,5,6,8} · {0,1,2,3,5,8,9}/{0,1,2,4,5,7,8} · {0,1,2,4,5,6,9}/{0,1,2,4,5,9,10} ·
{0,1,2,3,4,6,8,9}/{0,1,2,3,5,6,7,9}
(Note they come in complementary groups: the 4/8-note pair, and three 5/7-note pairs.)

Rev-2 note: these 8 families are exactly the Z12 families with k ∈ {4,5,7,8}, i.e. the k ≤ 5 classes
(Rosenblatt k=4, Erickson–Jones k=5) and their complements. For k = 5 no nontrivial 0/1 direct-sum
factorization exists (5 is prime), so "unexplained" here reflects the limits of the implemented moves,
not a gap in the literature.
