# Master Curriculum — The Roadmap

**Author:** Hedwig (mentor) · **Student:** Jigar · **v1** 2026-06-28

> This is a *living* document. We adjust based on evidence of what's
> sticking and what isn't. Nothing here is sacred except the principle:
> **understand deeply, don't just finish chapters.**

---

## 0. Diagnosis (why this plan looks the way it does)

| Dimension | Self-assessment | Implication for the plan |
|---|---|---|
| Python depth | Comfortable scripting, **hazy internals** | Dedicated internals track; lots of `id()`/`dis`/`sys` experiments |
| Math | **Rusty / mostly forgotten** | **Just-in-time math** woven into GenAI; no upfront bootcamp |
| Classical ML | Strong (production XGBoost/LightGBM) | Reuse as scaffolding; connect new ideas to known ones |
| Priority | "Mentor decides" | GenAI = main quest; Python = daily strength-training |
| Style | **Intuition first, then math** | Every concept: analogy → example → equation → code |

**The single biggest risk:** rusty math + wanting to read papers. The plan
*directly* mitigates this. If math becomes the bottleneck anyway, we slow the
paper track and thicken the math track. Evidence decides, not ego.

---

## 1. Daily structure (the 1–2 hour template)

Pick the variant that matches the day's energy/time:

### The 90-minute day (ideal)
- **0–10 min — Warm-up recall:** I quiz you on yesterday (active recall beats re-reading; see Roediger & Karpicke 2006, *Test-Enhanced Learning*).
- **10–70 min — Main quest (GenAI):** book section OR paper section + the just-in-time math it needs + a small coding task.
- **70–90 min — Python core:** one Fluent-Python concept + one hands-on internals experiment.

### The 60-minute day (busy)
- 5 min recall → 40 min GenAI → 15 min Python.

### The 30-minute day (survival)
- Either: finish one paper section's *intuition*, OR one Python experiment.
- **Never skip the recall.** Momentum > volume.

**Rule:** *every* session ends with one line in `PROGRESS_LOG.md`. No log, it
didn't happen. I audit the log weekly and call out skipped days.

---

## 2. The GenAI track — phases

We march through *Hands-On Large Language Models* (HOLLM) **interleaved** with
the paper sequence, so theory (papers) and practice (book/code) reinforce each
other. Full paper list + rationale: `PAPER_SEQUENCE.md`.

### Phase 1 — Foundations: how words become numbers (Weeks 1–3)
- **HOLLM Ch.1** Intro to Language Models; **Ch.2** Tokens & Embeddings.
- **Paper A:** Word2Vec — *Efficient Estimation of Word Representations* (Mikolov 2013).
- **Math JIT:** vectors, dot product, cosine similarity, vector spaces.
- **Code:** build embeddings, visualize them, do "king − man + woman ≈ queen".
- **Python parallel:** data model & objects (Ch.1 Fluent Python).

### Phase 2 — The road to the Transformer (Weeks 4–6)
- **Paper B:** Seq2Seq — *Sequence to Sequence Learning* (Sutskever 2014).
- **Paper C:** Attention — *NMT by Jointly Learning to Align & Translate* (Bahdanau 2014).
- **Math JIT:** matrix multiplication, softmax, weighted averages, gradients (intuition of backprop).
- **HOLLM Ch.3** Looking Inside LLMs (Transformers).
- **Code:** implement scaled dot-product attention from scratch in NumPy.

### Phase 3 — Attention Is All You Need (Weeks 7–9) ⭐
- **Paper D:** *Attention Is All You Need* (Vaswani 2017). **The big one.** We spend real time here.
- **Math JIT:** positional encodings (sinusoids), multi-head as parallel subspaces, LayerNorm.
- **Code:** mini-Transformer block in PyTorch (we'll install it properly).

### Phase 4 — Pretraining paradigms: BERT vs GPT (Weeks 10–12)
- **Paper E:** BERT (Devlin 2018) — bidirectional, masked LM.
- **Paper F:** GPT-2 (Radford 2019) — autoregressive, zero-shot.
- **HOLLM Ch.4** Text Classification; **Ch.11** Fine-tuning representation models.
- **Math JIT:** cross-entropy loss, perplexity, log-likelihood.
- **Code:** fine-tune a small BERT for classification (connect to your day-job intuition).

### Phase 5 — Scale, emergence, and instruction (Weeks 13–16)
- **Paper G:** GPT-3 — *Language Models are Few-Shot Learners* (Brown 2020).
- **Paper H:** Scaling Laws (Kaplan 2020) → Chinchilla (Hoffmann 2022).
- **Paper I:** InstructGPT / RLHF (Ouyang 2022).
- **HOLLM Ch.6** Prompt Engineering.
- **Code:** few-shot prompting experiments; measure how examples change output.

### Phase 6 — Reasoning, retrieval, efficiency (Weeks 17–20)
- **Paper J:** Chain-of-Thought (Wei 2022).
- **Paper K:** RAG (Lewis 2020).
- **Paper L:** LoRA (Hu 2021) — parameter-efficient fine-tuning.
- **HOLLM Ch.7** Advanced generation/agents; **Ch.8** Semantic Search & RAG; **Ch.12** Fine-tuning generation models.
- **Code:** build a small RAG pipeline; do a LoRA fine-tune.

### Phase 7 — Frontier & multimodal (Weeks 21+)
- **HOLLM Ch.9** Multimodal; **Ch.5/10** clustering & embedding models.
- **Papers (rotating):** Mixture-of-Experts, FlashAttention, DPO, vision-language (CLIP), and whatever's hot. We keep a "frontier queue."

> Timeline is *aspirational*, not a deadline. Depth wins. If Phase 3 takes 5
> weeks because the Transformer finally *clicks*, that's a win, not a slip.

---

## 3. The Python track

Runs every day as "strength training" (15–20 min). Goal: not "write code" but
*understand what the interpreter does*. Full roadmap: `PYTHON_CORE_TRACK.md`.
Spine = Fluent Python; depth = CPython-internals experiments.

---

## 4. ML & DL tracks
Placeholders (`03_ML/`, `04_DL/`). When you define objectives, I'll build them
the same way. **Heads-up:** much of the "DL track" will already be covered by
the GenAI math + Transformer work — we'll dedupe ruthlessly (DRY applies to
curricula too).

---

## 5. How Hedwig grades you (the harsh part)
- **Feynman test:** you must explain each concept back in plain English. If you can't, you don't know it yet.
- **Code-from-memory:** key algorithms (attention, embeddings) must be reproducible without copy-paste.
- **No hand-waving:** "it just attends to relevant tokens" is not an answer. *How?* Show the math.
- **Spaced repetition:** I'll re-quiz old material at random. Cramming gets exposed.

---

## 6. Tooling we'll set up (when needed)
- Python env via `uv` (not the Code Puppy venv).
- NumPy → PyTorch → Hugging Face `transformers`/`datasets`.
- Jupyter or plain scripts (your call) for experiments.

**Next action:** tell Hedwig *"start Day 1"* and we begin with embeddings +
the Python data model.
