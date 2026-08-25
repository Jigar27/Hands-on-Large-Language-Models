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

---

## Part 1c — Convexity taught + "why does unbounded magnitude destabilize training?" (session 2026-08-16)

### Follow-up A (verbatim — Jigar)
> "I dont know about convex combination and convex hull, so you probably add that
> in our maths syllabus."

**Action taken:** added **§3.5 — Convexity** to `00_Curriculum/MATH_PRIMER.md`.
**Taught:**
- **Convex combination** = weighted sum with all weights ≥ 0 AND summing to 1 (a
  "legal blend" — like mixing paint 50/30/20; result lives between the ingredients,
  can't overshoot them).
- **Convex hull** = smallest region enclosing a set of points (rubber band snapped
  around nails at each point).
- **Load-bearing fact:** a convex combination ALWAYS lands inside the convex hull.
  Non-negative + sum-to-1 is exactly the condition that cages the result. A
  negative weight or weights not summing to 1 lets the point escape the hull.
- **Tie to attention:** `c = Σ wᵢ vᵢ` with softmax weights is a convex combination of
  value vectors → `c` is caged inside the region of real history vectors.

### Follow-up B (verbatim — Jigar)
> "You said dot product can produce unbounded scores, how this unbounded magnitude
> scores makes training unstable?"

**Hedwig's answer — three failure chains:**
1. **Exploding activations → exploding gradients.** Unnormalized giant score → giant
   context vector `c` → magnitude compounds layer over layer. Backprop = chain
   rule = a PRODUCT of terms across layers; huge forward activations → huge
   derivative terms → gradient explodes to enormous values (or inf/NaN).
2. **Huge gradient → optimizer overshoots.** Update is `w ← w − lr·grad`. The learning
   rate assumes reasonably-sized gradients; a 10,000× gradient → a 10,000× step →
   catapults across the loss surface past the minimum → loss oscillates/diverges
   to NaN. Visible symptom = loss curve looks like a seismograph, not a slope.
3. **Scale-sensitivity → no consistent signal.** Magnitude of scores carries
   meaning it shouldn't; same relative relevances but different absolute sizes
   (longer vectors) → wildly different context magnitudes → model chases a moving
   target. Softmax's shift/scale-robustness removes this — only RELATIVE scores
   matter.

**How softmax fixes all three:** weights in (0,1) summing to 1 → `c` is a convex
combination → magnitude bounded by the value vectors (caged in convex hull) →
bounded activations → bounded gradients → fixed learning rate stays appropriate
→ loss descends smoothly. Causal chain snipped at the first link.

**New glossary term to bank:** exploding gradient.

---

## Part 2 — Drill SOLVED: softmax([2,1,0]) (session 2026-08-16)

`softmax([2, 1, 0])`, given `e²≈7.39, e¹≈2.72, e⁰=1`.

**Jigar's work:** sum = 11.107; w₁ = 7.39/11.107 = 0.67, w₂ = 0.25, w₃ = 0.09.
(Minor typo: wrote "7.39/10.107" but the result 0.67 proves he used 11.107.)
**Precise:** w = [0.665, 0.245, 0.090], sums to 1.000. Arithmetic CORRECT.

**The twist — Hedwig's drill framing was WRONG (sensei self-correction).**
Hedwig claimed softmax "sharpens" so the top weight lands ABOVE 0.67. Reality:
- Softmax top = 0.665; linear-normalization top = 2/3 = 0.667.
- Softmax top is actually SLIGHTLY BELOW linear's top. Claim busted by the numbers.

**Why:** softmax NEVER assigns exactly 0. Linear norm deleted the bottom element
(0/3 = 0) and dumped its mass on the top two; softmax gave the bottom 0.090, so
the top gets slightly less.

**Where sharpening actually shows up — the top/second RATIO:**
- Linear norm: 0.667/0.333 = 2.00
- Softmax:     0.665/0.245 = 2.71  → softmax WIDENED the #1-vs-#2 gap.

**Deeper takeaway:** softmax sharpness scales with the MAGNITUDE of the score
gaps. `[2,1,0]` (small gaps) → gentle. `[4,2,0]` → top rockets to ~0.87 (much
peakier). Same shape, bigger scale, sharper spotlight. This is exactly why the
Transformer divides by √d_k (§4) — to control sharpness and stop softmax
saturating into a hard one-hot. Jigar discovered the problem that scaling solves.

---

## Part 3 — Next up
Formalize Bahdanau attention from the softmax now fully owned.

---

## Part 4 — DEEP-DIVE: convexity + why unbounded scores destabilize training (session 2026-08-16)

### Trigger (verbatim — Jigar)
> "Actually, Convex combination and why unbounded scores destabilize training is
> yet to be covered in depth."

(He correctly flagged that Part 1c gave only an INTRO. This is the depth pass.)

---

### Part A — Convex combinations & convex hulls, in depth

**A.1 — Two points.** For points p, q: `r(t) = (1−t)p + t·q`, t ∈ [0,1].
- t=0 -> p; t=1 -> q; t=0.5 -> midpoint. Weights (1−t) and t are always ≥ 0 and
  always sum to 1. The set of all such r = the STRAIGHT SEGMENT between p and q.
- Break the rules: t=1.5 (weight >1, other weight −0.5 <0) -> r shoots PAST q,
  off the segment. t=−0.3 -> shoots off the other end. => non-negativity + sum-to-1
  is EXACTLY what confines you to the segment.

**A.2 — Three points.** `r = w₁p + w₂q + w₃s`, wᵢ≥0, Σwᵢ=1 -> the FILLED TRIANGLE
with corners p,q,s. Corners = pure weights [1,0,0] etc.; edges = one weight 0;
interior = all positive. Softmax weights [0.665,0.245,0.090] land inside, near p.

**A.3 — Formal defs.**
- Convex combination of v₁..vₙ = any Σ wᵢvᵢ with all wᵢ ≥ 0 and Σwᵢ = 1.
- Convex hull = set of ALL convex combinations = smallest convex set containing
  the points (rubber-band region).
- Convex set = for any two points in it, the whole segment between them is also
  in it (no dents/holes; disc convex, crescent not).

**A.4 — The boundedness THEOREM (the payoff).** If c = Σ wᵢvᵢ is a convex combo:
```
‖c‖ = ‖Σ wᵢ vᵢ‖  ≤  Σ wᵢ‖vᵢ‖  ≤  (Σ wᵢ)·max‖vᵢ‖  =  max‖vᵢ‖
```
PUNCHLINE: the context vector c can NEVER be longer than the longest value
vector. Mathematically caged inside the data.
- 1st ≤ : triangle inequality (always holds).
- 2nd ≤ : NEEDS wᵢ ≥ 0 (to pull the max out). A negative weight breaks THIS step;
  c can blow past max‖vᵢ‖.
- final = : NEEDS Σwᵢ = 1.
Both softmax properties are load-bearing in the proof. This is the rigorous
"caged in the convex hull" — the whole reason attention outputs are bounded.

---

### Part B — Why unbounded scores destabilize training, in depth
"Unstable" has TWO OPPOSITE failure modes; softmax touches both.

**B.1 — Mechanism 1: unbounded OUTPUTS -> EXPLODING gradients (compounding).**
Backprop = chain rule = a PRODUCT of per-layer factors. Each factor scales with
activation magnitude M. Across L layers the product scales like M^L — EXPONENTIAL
in depth. M=10, L=12 -> ~10^12 gradients -> weights lurch -> oscillate -> NaN.
With a convex-combination output, Part A pins ‖c‖ ≤ max‖vᵢ‖, so M is capped at the
DATA scale and can't grow layer-over-layer -> M^L stops exploding. The convexity
bound is EXACTLY what caps M, which is EXACTLY what prevents the blow-up.

**B.2 — Mechanism 2: unbounded SCORES INTO softmax -> VANISHING gradients.**
Softmax Jacobian diagonal: ∂wᵢ/∂sᵢ = wᵢ(1 − wᵢ). Zero at BOTH extremes
(wᵢ->0 and wᵢ->1), max at wᵢ=0.5. Huge scores SATURATE softmax (one weight ~1,
rest ~0 = hard one-hot) -> wᵢ(1−wᵢ) ~ 0 everywhere -> gradient through softmax
DIES -> training STALLS.
- Saturation = a squashing fn pushed so far into its flat region that its
  derivative ~0, so gradients can't flow back (same disease as sigmoid/tanh).
DOUBLE BIND: scores too big -> saturate -> vanishing; unbounded outputs fed
forward -> exploding.

**B.3 — Mechanism 3: raw numerical overflow.** e^1000 = inf in float32;
inf/inf = NaN; one NaN contaminates the whole net. Fix: subtract the max score
first (softmax(z) = softmax(z − max z), valid by shift-invariance) -> largest
exponent becomes e^0 = 1, dodging overflow.

**B.4 — Lands on √d_k (hook to §4).** Dot products q·k in d dims grow ~√d
(unit-scale entries). d=512 -> scores ~√512 ≈ 23 -> deep in saturation (Mech 2).
Dividing by √d_k rescales scores to ~unit -> softmax stays in its healthy
high-gradient region. => derived the exact disease √d_k cures (that's §4).

---

### OPEN Feynman-gate questions (Jigar to answer NEXT SESSION)
1. In the bound ‖c‖ ≤ max‖vᵢ‖, WHICH step breaks if a weight is negative, and what
   goes wrong geometrically?
2. Unbounded scores -> VANISHING gradients through softmax, but EXPLODING
   gradients when fed forward as activations. One sentence each: why opposite
   directions?

### OFFERED (not yet done): hands-on NumPy experiment — watch a convex combo stay
caged inside the triangle while a non-convex one escapes; watch softmax gradients
collapse (wᵢ(1−wᵢ) -> 0) as scores grow. Jigar to decide next session.

### New glossary term to bank: Saturation.

---

## Part 5 — Next up (after the open questions above)
Formalize Bahdanau attention from the softmax now fully owned; then §4 (matrices,
scaled dot-product attention, √d_k).

