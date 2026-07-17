# Day 2 Session Transcript — 2026-07-12

> A record of the *interactive exchange* (Jigar's answers + Hedwig's teaching),
> so the back-and-forth isn't lost. Summary lives in `PROGRESS_LOG.md`; the
> runnable code lives in `01_GenAI/code/` and `02_Python/experiments/`.

---

## Part 0 — Recall quiz (Day 1 spaced repetition)

**Q1 — Dot product.** `a=[3,1]`, `b=[2,4]` → `a·b`?
- **Jigar:** `(3×2)+(1×4) = 10`.  Correct.

**Q2 — Cosine meaning at +1 / 0 / −1.**
- **Jigar:** +1 = similar, same direction; 0 = perpendicular, low similarity;
  −1 = opposite, 180°, not similar.  (calibration: 0 = *no*/unrelated, not "low")

**Q3 — Perpendicular test.**
- **Jigar:** dot product = 0, or angle = 90°.  Correct.

**Q4 — Why `king − man + woman ≈ queen`.**
- **Jigar:** King is a vector in n-dim space; each dimension encodes attributes of
  meaning. Subtracting Man removes the gender/manness dimensions while keeping
  Royalty intact; adding Woman injects female attributes onto Royalty → lands
  near Queen.  Excellent — graduate-level phrasing.

**Q5 — Aliasing.** `a=[1,2,3]; b=a; b.append(4); print(a)`
- **Jigar:** `a` is a reference to `[1,2,3]`; `b=a` makes a second reference to the
  same object → `print(a)` = `[1,2,3,4]`.  Correct.

**Q6 — Interning vs constant folding.**
- **Jigar:** "I don't know." (honest — the right move)

---

## Part 1 — Debt cleared: interning vs constant folding

- **Jigar observed:** on his machine, BOTH `256 is 256` and `257 is 257` return True.
- **Hedwig:** that's the lesson, not a contradiction:
  - **Interning** = CPython caches & reuses one object for small ints (−5..256)
    and short strings. Explains 256.
  - **Constant folding** = compile-time; the compiler stores one shared `257`
    literal within a code block → `257 is 257` on one line is True *despite* 257
    not being interned. Different mechanism, same visible result.
- **Experiment to break it:** `x=257; y=int("257")` (runtime value defeats folding).
  - **Jigar predicted:** `x==y` True (compares value), `x is y` False (compares
    identity).  Both correct.
  - **Reality:** `x==y -> True`, `x is y -> False`, `id(x) != id(y)` (two objects).
- **Rule:** `is` = same object; `==` = same value. Use `==` for values; reserve
  `is` for `None`/singletons.

---

## Part 2 — GenAI Math Primer §2: weighted sums & hidden states

**Drill A — weighted sum.** `w=[0.1,0.6,0.3]`, `x=[2,5,-1]`.
- **Jigar:** `0.2+3−0.3 = 2.9`; weights sum to 1 → treat as probabilities
  (→ it's a weighted *average*).  (previews softmax)

**Drill B — hidden state update.** `h=W_h·h_prev + W_x·x`, `h_prev=3, x=2, W_h=0.5, W_x=1.0`.
- **Jigar:** `1.5+2 = 3.5`. 

**Drill C — Feynman: why is one hidden state a problem?**
- **Jigar:** if a sentence is large, the decoder doesn't have enough info to work with.
- **Hedwig sharpened:** fixed-size vector for variable-length input = information
  bottleneck; early words fade. Then pushed for the *second half*: what would you
  WANT the decoder to do instead?

**The decisive exchange (Jigar pre-invents attention):**
- **Jigar:** "If the decoder can see all encoder hidden states, it can check the
  dot product of its current state against each encoder state (target word vector)."
- **Hedwig:** YES. That's attention. current decoder state = **query**, each
  encoder state = **key**, averaged thing = **value**;
  `softmax(query·keys) → weights → weighted sum of values`.

**Jigar's sharp question:** if all training sentences are similar length, why can't
the net just learn to squash into a fixed vector well enough?
- **Hedwig's answer — three reasons uniform length doesn't save you:**
  1. **Capacity ceiling** — fixed dims hold finite info; equal length ≠ equal content.
  2. **Vanishing gradients** — early words can't be *trained* to survive many steps
     (learnability ≠ representational capacity).
  3. **Static vs dynamic focus (the killer)** — one context vector is reused for
     every output word, but different output words need different input words.
     Attention builds a fresh, per-step context.

---

## Part 3 — Python: the mutable default argument trap

**Setup:** `def add_item(item, bag=[]): bag.append(item); return bag`
- **Jigar predicted:** default created at call time, but "due to constant folding"
  all items append to the same list.
- **Reality:** outputs accumulate → `['apple']`, `['apple','banana']`,
  `['apple','banana','cherry']`. Correct *output*, wrong *reasoning*.
- **Hedwig corrected two bugs:**
  1. NOT constant folding (that's compile-time for immutable literals; `[]` is
     mutable, never folded).
  2. Timing was backwards — the accumulation PROVES the default is created
     **once, at definition time**, and stored on `func.__defaults__` (one shared
     list). This is Day-1 aliasing in disguise.
- **Fix — None sentinel:**
  ```python
  def add_item_safe(item, bag=None):
      if bag is None:      # 'is' correct here: None is a singleton
          bag = []         # fresh list per call, built in the body
      bag.append(item)
      return bag
  ```
- **Feynman gate:**
  - **Jigar:** (1) default created once at def time; (2) `bag=None` stores no list
    on the function; a fresh list is created (and later GC'd) each call.  Both correct.

---

## Where we left off
- **Next menu:** §3 softmax → formalize attention (Bahdanau); OR real pretrained
  embeddings (gensim); OR Python Module 2 / `__defaults__` & closures follow-up.
