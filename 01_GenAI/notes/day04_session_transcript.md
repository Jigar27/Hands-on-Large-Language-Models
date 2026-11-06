# Day 4 Session Transcript — 2026-09-27

> Interactive record. Returning after a ~6-week gap (last session 2026-08-16).

---

## Part 0 — Re-entry: recall + review

### Q1 (verbatim — Jigar)
> "Can you load question and answers I have for the last topic"

**Hedwig:** Presented all Day 3 softmax Q&As from `day03_session_transcript.md`
(Q1, Q2, Q3, Follow-ups A/B, drill, deep-dive trigger) + the 2 open Feynman
questions. Flagged two over-statements in the Day 3 notes:
- "softmax is the *unique* simple converter" -> too strong; it's the *standard*
  choice (alternatives exist, e.g. sparsemax).
- "sum-to-1 makes it a convex combination" -> only *together with* wᵢ ≥ 0.

### Q2 (verbatim — Jigar)
> "Can you please revise the attention mechanism, so that I can recall why I have
> asked these quetions?"

**Hedwig's answer — attention as a story, with each Day 3 question pinned to the
step that raised it:**

1. **Problem (Day 2):** Seq2Seq encoder squashes the whole sentence into ONE
   fixed-size vector -> bottleneck; early words fade; same context reused for
   every output word (static focus).
2. **Idea (Jigar's own, Day 2):** keep ALL encoder hidden states h₁..hₙ; at each
   decoder step, compare current decoder state against each one.
3. **Mechanism — 3 steps:**
   - Score:  sᵢ = q · kᵢ       (q = decoder state, kᵢ = encoder states)
   - Weight: wᵢ = softmax(s)ᵢ
   - Blend:  c = Σ wᵢ vᵢ       (fresh context vector per output word)
4. **Where each question came from:** Step 1->2 gap = "why not use sᵢ directly?"
   (Q1), "what about negative sᵢ?" (Q2), "organize it" (Q3); Step 3 output =
   "why must c be bounded?" (convexity, Follow-up A) and "why do big scores break
   training?" (Follow-up B, deep-dive).
5. **Worked example (computed):** unit vectors h₁=(1,0), h₂=(0,1), h₃=(−1,0),
   scores s=[2,0,−2].
   - softmax -> w=[0.867, 0.117, 0.016]; c=(0.851, 0.117), ‖c‖=0.859 ≤ 1  (caged)
   - raw scores as weights -> c = 2·h₁ + 0·h₂ − 2·h₃ = (4, 0), ‖c‖=4  (escaped
     hull; the −2 weight on h₃ = "anti-relevant" vector mirrored and ADDED,
     pushing c further along h₁ — the fly-away effect).
