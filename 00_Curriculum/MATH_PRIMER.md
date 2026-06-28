# Just-In-Time Math Primer

**Philosophy:** You said your math is rusty. We do **not** fix that with a
6-month course that kills your momentum. We fix it with *small, targeted
doses* delivered the same week you need them — intuition first, then the
symbols. Each section below is unlocked right before the paper that requires it.

> Reminder of *why* this matters: you cannot truly understand attention
> without the dot product and softmax. Not "kind of." We do this properly.

---

## §1 — Vectors & similarity  (unlocks: Word2Vec, embeddings)
- **Intuition:** a vector is an arrow / a list of numbers / a point in space. A word embedding is a point; similar words are nearby points.
- **Concepts:** vector, dimensions, magnitude (length), **dot product**, **cosine similarity**, vector addition/subtraction.
- **The "aha":** dot product ≈ "how much do two arrows point the same way." Cosine similarity = dot product normalized by lengths → a similarity score in [-1, 1].
- **Drill:** by hand, compute the dot product and cosine of [1,2] and [2,1]. Then in NumPy. Then do `king - man + woman`.

## §2 — Weighted sums & hidden states  (unlocks: Seq2Seq)
- **Intuition:** a "hidden state" is the model's running memory, a vector summarizing what it's seen so far.
- **Concepts:** weighted sum, linear combination, the idea of compressing a sequence into a vector (and why that's lossy).

## §3 — Softmax & weighted averages  (unlocks: Attention / Bahdanau)
- **Intuition:** softmax turns a list of raw scores into probabilities that sum to 1 — a "spotlight" that brightens the biggest scores.
- **Concepts:** exponentials, normalization, softmax formula, attention as a *softmax-weighted average of value vectors*.
- **Drill:** compute softmax of [2, 1, 0] by hand; confirm it sums to 1; note how it exaggerates the largest.

## §4 — Matrices & the Transformer core  (unlocks: Attention Is All You Need)
- **Intuition:** a matrix multiply = applying the same linear transformation to many vectors at once (this is why GPUs love it).
- **Concepts:** matrix multiplication (shapes!), Q/K/V projections, scaled dot-product attention `softmax(QKᵀ/√d_k)V`, why we divide by √d_k (keeps the softmax from saturating), multi-head = several attention "views" in parallel subspaces, positional encoding (sinusoids), LayerNorm (intuition only).
- **Drill:** implement `softmax(QKᵀ/√d_k)V` in NumPy on tiny matrices and trace the shapes.

## §5 — Loss & training signal  (unlocks: BERT, GPT, all training)
- **Intuition:** cross-entropy measures "how surprised the model was by the right answer." Lower = better. This is the number gradient descent pushes down.
- **Concepts:** probability, log-likelihood, **cross-entropy loss**, **perplexity** (= exp of average loss; "how many words is the model effectively choosing between").
- **Bridge to your day job:** this is the classification-loss cousin of the log-loss your XGBoost/LightGBM models optimize. You already have the intuition — we're just naming it.
- **Drill:** compute cross-entropy for a 3-class prediction by hand.

## §6 — Rank & low-rank decomposition  (unlocks: LoRA)
- **Intuition:** a big matrix can often be *approximated* by multiplying two skinny matrices — far fewer numbers, almost the same effect. LoRA trains those skinny matrices instead of the giant one.
- **Concepts:** matrix rank (light), low-rank approximation, parameter count savings.

## §7 — Gradients & backprop  (running theme, deepened over Phases 2–4)
- **Intuition:** the gradient points "uphill"; we step the opposite way to reduce loss. Backprop is just the chain rule applied efficiently across layers.
- **Concepts:** derivative as slope, partial derivatives, chain rule, gradient descent, learning rate.
- **Bridge:** boosting (your world) and neural nets both descend a loss surface; different machinery, same goal.

---

## Standing rule
Whenever a paper throws a symbol you don't recognize, **write it in your notes
and tell me.** Unknown notation is not a failure — *pretending* you understood
it is. I'd rather spend 15 minutes on a sigma than let you fake it.
