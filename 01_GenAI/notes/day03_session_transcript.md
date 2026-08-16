# Day 3 Session Transcript — 2026-08-08

> Interactive record. Summary goes in `PROGRESS_LOG.md` at session end;
> runnable code lives in `02_Python/experiments/` and `01_GenAI/code/`.

---

## Part 0 — Carry-over Q&A from Day 2 debrief (mutable defaults deep-dive)

**Jigar's Q1:** We solved the mutable-default-arg bug with `None` (immutable).
Is an immutable default ALSO created once and stored on the function object,
same as a mutable one? And would ANY immutable object fix the bug the same way?

- **Experiment (`m2_immutable_defaults.py`):** `func.__defaults__` shows a
  tuple built once at `def` time for ALL defaults regardless of mutability --
  `([],)` for a mutable list, `((),)` for an immutable tuple, `(None,)` for
  None. No special-casing of None here.
- **Split the bug in two:**
  - **Accumulation bug:** ANY immutable default fixes this (can't mutate in
    place -> operations like `bag + (item,)` build a new object and rebind).
  - **Sentinel-safety bug (the twist):** immutability alone is NOT enough.
    `pct=0` used as a "nothing passed" sentinel silently overrides a caller who
    genuinely means `0` (`set_discount_bad(0)` wrongly returns 5). `None`
    works because it's a value no real caller ever means as actual data.
- **Conclusion:** immutability solves accumulation; semantic uniqueness
  (sentinel-safety) is a separate property. `None` happens to have both.

**Jigar's Q2:** What even IS a "sentinel"? And why `is None` instead of
`== None`?

- **Sentinel, plain language:** a marker object whose only job is to mean
  "no real value was given here" -- like the flag on a mailbox. Must be a
  value no caller would ever legitimately pass as real data (why `0`/`""`
  make bad sentinels but `None` is good).
- **`is` vs `==` experiment (`m3_is_none_vs_eq_none.py`):** a `YesMan` class
  that overrides `__eq__` to always return `True` makes `ym == None` lie
  (`True`, even though `ym` is clearly not None). `ym is None` correctly says
  `False` and cannot be fooled -- `is` is raw identity comparison, immune to
  any class's custom `__eq__`.
- **Real-world hazard flagged:** `numpy_array == None` returns an elementwise
  array of bools, not one bool, and crashes `if` statements built on it
  (`ValueError: truth value of an array is ambiguous`) -- a live landmine in
  ML code. `arr is None` stays a clean single bool.

**Jigar's follow-up (self-correction moment):** "So `is` is better than `==`,
but it only works because None is a singleton." -- **Corrected:**

- **Experiment (`m4_is_vs_eq_general_rule.py`):** two equal-but-distinct lists
  `a=[1,2,3]` and `b=[1,2,3]` give `a == b -> True` but `a is b -> False`. If
  `is` were "generally better," this would be a bug -- it isn't, because `is`
  correctly answered a DIFFERENT question ("same object?") than the one
  Jigar actually wanted ("same value?").
- **Reframed rule:** `is` and `==` ask different questions; they only agree
  when identity and equality collapse into the same thing, which happens
  ONLY for singletons (`None`, `True`, `False`). For everything else
  (numbers, strings, lists, custom objects), `==` is the correct tool.
- **Final rule banked:** `is` for singleton checks (`None`/`True`/`False`);
  `==` for value comparisons everywhere else. Not a hierarchy of "better" --
  a matter of which question you're actually asking.

**New glossary terms added:** Singleton, Sentinel value.

---

## Part 1 — GenAI Math Primer §3: softmax (session 2026-08-15)

> NOTE ON PROVENANCE: Jigar's two questions below are recorded **verbatim**
> (recalled by him on 2026-08-16). Hedwig's answers are **reconstructed** from
> kennel memory of the original replies — faithful in substance, not word-for-word.

### Q1 (verbatim — Jigar)
> "Why softmax is needed? why cant we work with raw dot product scores as
> weights itself. why do we need weights which sum to 1."

**Hedwig's answer (reconstructed):**
Raw dot-product scores fail as weights on several counts, and softmax fixes all
of them at once:
- **Not positive** — dot products can be negative, and a negative "weight" in a
  weighted average is nonsensical (you'd be *subtracting* a value's contribution
  rather than down-weighting it).
- **Not bounded / arbitrary scale** — raw scores can be any size; magnitudes
  depend on vector lengths, so they aren't comparable as "shares of attention."
- **Don't sum to 1** — without normalization the result of the weighted sum can
  explode or shrink arbitrarily; it's no longer an *average*.
- **Why sum-to-1 specifically:** it makes the output a **convex combination** —
  a true weighted average that stays in-bounds relative to the inputs, and is
  readable as a probability distribution ("how much attention to pay to each").
- Softmax also gives **differentiability** (trainable by gradient descent) and
  **scale-robustness** (shift-invariance: adding a constant to all scores leaves
  the output unchanged).

### Q2 (verbatim — Jigar)
> "If dot product is negative, softmax is turning it to positive value through e
> raise to value. You also explained me the difference between irrelevant and
> anti relevant."

**Hedwig's answer (reconstructed):**
- `e^x` is **always positive** for any real `x`, so `e^(negative)` is a small
  *positive* number, never negative. `e^-5 ≈ 0.0067`.
- "Opposite direction" (negative dot product) does NOT mean "negative weight that
  subtracts." It means "smallest positive weight → effectively ignored."
- **Irrelevant vs anti-relevant** (the distinction Jigar flagged):
  - **Irrelevant** — dot product ≈ 0 (perpendicular / unrelated). `e^0 = 1`.
  - **Anti-relevant** — dot product strongly negative (points the opposite way).
    `e^(negative)` → an even *tinier* positive weight than the irrelevant one.
  - Both get down-weighted toward ~0, but softmax preserves their **ranking**
    (it's **monotonic**): anti-relevant lands below irrelevant lands below
    relevant. Softmax never *subtracts* a value; it only decides how little
    spotlight each one gets.

**Glossary terms banked this session:** convex combination, convex hull,
monotonic, softmax shift-invariance, and the "why exponentiate" trio.

---

## Part 1b — The full "why softmax" synthesis (Q3, session 2026-08-16)

### Q3 (verbatim — Jigar)
> "Please organize your thoughts and motivate the use of softmax" — asking for a
> single organized argument pulling together: training instability, convex
> combination of vectors, why linear normalization fails (divide-by-zero + other
> problems), and why negative dot-product scores make the context vector fly away
> in the opposite direction of the history vector that produced them.

**Hedwig's answer — the organized motivation:**

**Setup.** Attention computes a context vector `c = Σᵢ wᵢ vᵢ` (weighted blend of
value vectors). Raw scores are `sᵢ = q · kᵢ`. The whole question: how do we turn
raw scores `sᵢ` into weights `wᵢ`?

**Step 1 — What the weights MUST satisfy:**
| # | Requirement | Why |
|---|---|---|
| 1 | Non-negative (`wᵢ ≥ 0`) | negative weight subtracts a value → context flies away from that history vector |
| 2 | Sum to 1 | makes `c` a convex combination (a true bounded average) |
| 3 | Monotonic | bigger relevance → bigger weight (preserve ranking) |
| 4 | Differentiable | trained by gradient descent |
| 5 | Numerically stable | no divide-by-zero, no blow-ups, scale-robust |

**Step 2 — Candidate A: raw dot products as weights (`wᵢ = sᵢ`).**
- Fails non-negativity: if `sⱼ < 0` then `wⱼ vⱼ` points OPPOSITE to `vⱼ` — an
  anti-relevant vector actively shoves `c` away from itself instead of being
  ignored. "Irrelevant" should mean "don't include" (weight→0), NOT "include its
  mirror image."
- Fails sum-to-1: magnitude of `c` uncontrolled → activations/gradients explode
  → **training unstable.**

**Step 3 — Candidate B: linear normalization (`wᵢ = sᵢ / Σⱼ sⱼ`).** Fails 3 ways:
- (a) **Divide-by-zero** — scores that cancel (e.g. `[3,−3]`, sum 0) → undefined;
  near-zero sums → weights explode. Fatal.
- (b) **Negative weights survive** — `[5,−3]`→sum 2→`[2.5,−1.5]`: the −1.5 still
  causes fly-away; the 2.5 is out of [0,1]. Sum-to-1 only cosmetically satisfied.
- (c) **Sign flips** — if the sum is negative, every sign flips; the most relevant
  vector can get a negative weight. Ranking inverts.

**Step 4 — Candidate C: softmax (`wᵢ = e^{sᵢ} / Σⱼ e^{sⱼ}`).** Clears everything:
1. Non-negative: `e^x > 0` always → `wᵢ ∈ (0,1)`; anti-relevant → tiny positive
   weight (dropped, never mirrored). No fly-away possible.
2. Sums to 1 by construction → convex combination.
3. Denominator is a sum of strictly-positive exponentials → ALWAYS > 0 →
   **the divide-by-zero that kills linear normalization cannot occur.**
4. Monotonic (and sharpens big gaps — the spotlight effect).
5. Differentiable everywhere → trainable.
6. Shift-invariant → subtract the max for numerical stability, answer unchanged.

**Step 5 — Geometric punchline.** Requirements 1+2 = a **convex combination**,
which is guaranteed to land INSIDE the **convex hull** of the value vectors
(rubber band around all points `v₁…vₙ`). So `c` can never escape the region
spanned by the actual history vectors — bounded magnitude → no explosions, no
fly-away → **stable training.** Candidates A and B let `c` break out of the hull;
only softmax cages it.

**One-sentence motivation:** softmax is the unique simple converter that turns
arbitrary real-valued relevance scores into a valid convex combination — strictly
positive, summing to one, monotonic, smooth, divide-by-zero-proof — so the context
vector stays a bounded, stable blend of the real history vectors instead of an
exploding, sign-flipping, or fleeing mess.

---

## Part 2 — Pending drill (still open)

`softmax([2, 1, 0])` by hand, given `e²≈7.39, e¹≈2.72, e⁰=1`:
- the three weights, do they sum to ~1,
- and the sharpening test: does the top score land above or below `2/3 ≈ 0.67`?

