# Research Paper Sequence — Read In This Order (and here's WHY)

**Curated by Hedwig.** This is *not* the raw order papers were published, and
it's *not* just "whatever the book cites." It's a **pedagogical** order: each
paper makes the next one readable. Reading the Transformer paper before you
understand attention is like reading the last chapter of a mystery novel first.

For each paper you get: the one-line idea, why it matters, the math you need
first (linked to `MATH_PRIMER.md`), and what you should be able to explain
afterward.

---

## Tier 0 — Why these and not "just the famous ones"?
The famous papers (Transformer, GPT-3) *depend* on ideas from earlier, less
famous ones (embeddings, attention, seq2seq). We build the dependency chain
bottom-up. Skipping rungs is how people end up quoting papers they can't
actually explain.

---

## Phase 1 — Representations

### Paper A — Word2Vec
- **Mikolov et al., 2013** — *Efficient Estimation of Word Representations in Vector Space.*
- **One line:** words become dense vectors where geometric distance = semantic similarity.
- **Why first:** *everything* in LLMs is vectors. This is the conceptual atom.
- **Math first:** vectors, dot product, cosine similarity. (Primer §1)
- **You must be able to explain:** why `king - man + woman ≈ queen` works; what the dot product is measuring.

---

## Phase 2 — The road to attention

### Paper B — Seq2Seq
- **Sutskever et al., 2014** — *Sequence to Sequence Learning with Neural Networks.*
- **One line:** an encoder RNN compresses a sentence into one vector; a decoder RNN unrolls it into another sequence.
- **Why:** introduces the encoder–decoder framing the Transformer later revolutionizes. Also exposes the *bottleneck problem* (one vector for a whole sentence) that motivates attention.
- **Math first:** weighted sums, intro to hidden states. (Primer §2)
- **Explain afterward:** what the "fixed-length bottleneck" is and why it's bad for long sentences.

### Paper C — Attention (Bahdanau)
- **Bahdanau et al., 2014** — *Neural Machine Translation by Jointly Learning to Align and Translate.*
- **One line:** instead of one bottleneck vector, let the decoder *look back* at all encoder states, weighted by relevance.
- **Why:** this is the literal birth of attention. The Transformer is "what if attention were the *whole* model?"
- **Math first:** softmax, weighted averages. (Primer §3)
- **Explain afterward:** what the attention weights represent; why softmax turns scores into a "spotlight."

---

## Phase 3 — The Transformer (the keystone)

### Paper D — Attention Is All You Need
- **Vaswani et al., 2017.**
- **One line:** drop recurrence entirely; build the model from self-attention + feed-forward layers, fully parallelizable.
- **Why:** the foundation of *every* modern LLM. We spend 2–3 weeks here. No rushing.
- **Math first:** matrix multiplication, scaled dot-product, multi-head intuition, positional encodings, LayerNorm. (Primer §4)
- **Explain afterward:** Q/K/V in your own words; why we divide by sqrt(d_k); why multi-head ≠ one big head; how position is injected without recurrence.
- **Deliverable:** implement scaled dot-product attention from scratch.

---

## Phase 4 — Pretraining paradigms

### Paper E — BERT
- **Devlin et al., 2018** — *BERT: Pre-training of Deep Bidirectional Transformers.*
- **One line:** encoder-only Transformer pretrained by masking words and predicting them; great for *understanding* tasks.
- **Why:** the "understanding/representation" branch. Maps directly to your day-job classification instincts.
- **Math first:** cross-entropy loss. (Primer §5)
- **Explain afterward:** masked LM vs next-sentence prediction; why "bidirectional" matters.

### Paper F — GPT-2
- **Radford et al., 2019** — *Language Models are Unsupervised Multitask Learners.*
- **One line:** decoder-only Transformer trained to predict the next token; scales into a surprisingly general zero-shot learner.
- **Why:** the "generation" branch — the ancestor of ChatGPT.
- **Explain afterward:** autoregressive generation; why decoder-only differs from BERT; what "zero-shot" means here.

---

## Phase 5 — Scale & alignment

### Paper G — GPT-3
- **Brown et al., 2020** — *Language Models are Few-Shot Learners.*
- **One line:** make it *huge* (175B params) and in-context/few-shot learning emerges.
- **Explain afterward:** in-context learning; few-shot vs fine-tuning.

### Paper H — Scaling Laws + Chinchilla
- **Kaplan et al., 2020** — *Scaling Laws for Neural Language Models.*
- **Hoffmann et al., 2022** — *Training Compute-Optimal LLMs (Chinchilla).*
- **One line:** performance is a predictable function of compute/data/params — and most big models were *undertrained* on data.
- **Why:** explains the entire industry's behavior; deeply practical.
- **Explain afterward:** the compute-optimal data/param trade-off; why Chinchilla "beat" bigger models.

### Paper I — InstructGPT / RLHF
- **Ouyang et al., 2022** — *Training LMs to Follow Instructions with Human Feedback.*
- **One line:** align raw LLMs to human intent via supervised fine-tuning + reward model + RL.
- **Why:** the bridge from "GPT-3" to "ChatGPT." This is *the* alignment paper.
- **Explain afterward:** the 3-step RLHF pipeline; what the reward model does.

---

## Phase 6 — Reasoning, retrieval, efficiency

### Paper J — Chain-of-Thought
- **Wei et al., 2022** — *Chain-of-Thought Prompting Elicits Reasoning in LLMs.*
- **One line:** ask the model to "think step by step" and reasoning performance jumps.

### Paper K — RAG
- **Lewis et al., 2020** — *Retrieval-Augmented Generation.*
- **One line:** bolt a retriever onto a generator so the model can cite external knowledge.
- **Why:** the dominant pattern in production GenAI today.

### Paper L — LoRA
- **Hu et al., 2021** — *LoRA: Low-Rank Adaptation of Large Language Models.*
- **One line:** fine-tune giant models by training tiny low-rank adapter matrices.
- **Math first:** matrix rank, low-rank decomposition (light). (Primer §6)

---

## Phase 7 — Frontier queue (rotating, we curate as we go)
- **CLIP** (Radford 2021) — vision-language contrastive learning.
- **FlashAttention** (Dao 2022) — making attention fast/memory-efficient.
- **Mixture-of-Experts** (e.g. Switch Transformer, Fedus 2021).
- **DPO** (Rafailov 2023) — RLHF without the RL.
- ...and whatever the field births while we study. We'll add them here.

---

## How to read a paper (the method I'll enforce)
1. **Pass 1 (10 min):** title, abstract, figures, conclusion. Get the gist.
2. **Pass 2 (30 min):** intro + method, skip heavy proofs. Note every symbol you don't know.
3. **Pass 3 (deep):** we go through the math together; you re-derive the key equation.
4. **Feynman:** you explain it to me in plain English. I poke holes.
5. **Code:** reproduce the smallest core idea in code.

(Adapted from Keshav's *"How to Read a Paper"* — itself worth reading once.)
