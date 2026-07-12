# Progress Log

**Rule:** one entry per study session. No entry = it didn't happen. Hedwig
audits this weekly and will absolutely call out gaps. Honesty over optics —
"struggled with softmax" is a *better* entry than "finished chapter 3."

Format:
```
## YYYY-MM-DD  (minutes)
- Track: GenAI / Python / Math
- What I covered:
- What clicked:
- What confused me (be specific — name the symbol/concept):
- Feynman check (could I explain it aloud? y/n):
- Next:
```

---

## 2026-06-28  (setup)
- Track: Meta
- What I covered: Met my mentor (Hedwig). Curriculum, paper sequence, math
  primer, and Python track created. Diagnosis: hazy Python internals, rusty
  math, strong classical-ML base.
- Next: Day 1 — embeddings intuition + Python object model.

<!-- New entries below this line -->

## 2026-07-06  (~90 min)
- Track: GenAI (Math Primer §1) + Python (Module 1)
- What I covered: Embeddings intuition — vectors, dot product, magnitude, cosine
  similarity; perpendicularity (dot=0). Built & ran `01_GenAI/code/day01_similarity.py`
  (confirmed hand calcs; ran king−man+woman→queen). Python object model — names vs
  objects, aliasing, `is` vs `==`, interning vs constant folding
  (`02_Python/experiments/m1_names_vs_objects.py`).
- What clicked: dot product = 4, cosine = 0.8; engineered a perpendicular vector
  (−3, 4.5); predicted aliasing result [1,2,3,4] correctly from the model.
- What confused me: (be honest, fill in) — initially over-claimed cosine 0.8 as
  "nearly identical" (it's ~37°, strongly similar not identical); the perpendicular
  question phrasing at first; the 257-is-257 surprise (constant folding vs interning).
- Feynman check: y for dot/cosine/perpendicular & aliasing; revisit interning vs
  folding aloud next session.
- Next: Math Primer §2 (weighted sums / hidden states) toward Seq2Seq, OR real
  pretrained embeddings (gensim) for a non-toy analogy; Python Module 1 cont.
  (mutable default args trap) or Module 2.

## 2026-07-12  (~90 min)
- Track: GenAI (Math Primer §2) + Python (Module 1 cont.)
- What I covered: Day 1 recall quiz (dot product, cosine meaning, orthogonality,
  king−man+woman, aliasing) — all passed. Cleared the interning-vs-constant-folding
  debt (proved `257 is 257` True via folding, but `x=257; y=int("257")` gives
  `is` False with different ids). GenAI §2: weighted sums / linear combinations,
  hidden state as running memory, RNN update `h_t = f(W_h h_{t-1} + W_x x_t)`,
  Seq2Seq + the information bottleneck. Python: the mutable default argument trap
  (`bag=[]`) + the `None`-sentinel fix.
- What clicked: weights summing to 1 = a weighted *average* (preview of softmax);
  pre-derived the attention mechanism unprompted (dot-product decoder state vs each
  encoder hidden state -> softmax weights -> weighted average = query/key/value);
  saw mutable-default trap as Day-1 aliasing in disguise (default lives on
  `func.__defaults__`, created once at def time).
- What confused me (honest): first attributed the mutable-default bug to "constant
  folding" and thought the default was created at call time — corrected: defaults
  are evaluated ONCE at definition time; folding is compile-time for immutable
  literals only. Also asked a sharp question: why not just learn to squash into a
  fixed vector if lengths are uniform? (Answer: capacity ceiling + vanishing
  gradients + static-vs-dynamic focus.)
- Feynman check: y for weighted sum, hidden state, Seq2Seq bottleneck, is-vs-==,
  interning vs folding, mutable defaults + None fix.
- Next: Math Primer §3 (softmax & weighted averages) -> formalize attention
  (Bahdanau), OR real pretrained embeddings (gensim). Python: Module 2 (or the
  `__defaults__`/closures follow-up).
