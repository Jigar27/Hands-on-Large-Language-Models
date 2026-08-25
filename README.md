# Hedwig's Dojo

> **Journey name:** *Hedwig's Dojo* (our master recall handle -- say it to resume
> the whole arc). Spine text: *Hands-On Large Language Models*.
> Mentored by **Hedwig** (harsh, evidence-first critic; never flatters).
> Started: 2026-06-28.
>
> **Progress:** Day 1 (2026-07-06) + Day 2 (2026-07-12) complete. Per-day
> interactive transcripts live in `01_GenAI/notes/dayNN_session_transcript.md`.

This repo doubles as (1) my working copy of **Hands-On Large Language Models**
(Alammar & Grootendorst) and (2) my structured path from "production ML
practitioner" to "person who deeply understands GenAI, Python internals, ML and
DL — from first principles to the frontier."

## The Four Tracks
1. **GenAI** — *main quest.* Hands-On LLMs + a curated research-paper sequence,
   explained intuition-first with worked examples and code.
2. **Python** — language *core*: object model, memory model, what actually
   happens when I create a list/dict/object. Fluent Python (Ramalho) +
   CPython-internals experiments.
3. **ML** — *(objectives TBD; placeholder structure ready)*.
4. **DL** — *(objectives TBD; placeholder structure ready)*.

## How this works (the contract)
- **Cadence:** 1-2 hours/day. Hedwig tells me what to read/learn/code each day.
- **Hidden prerequisite:** my math is rusty, so a **just-in-time math primer**
  is woven into the GenAI track — small doses, right before each paper needs it.
- **Learning style:** intuition/analogy first, *then* the equations and rigor.
- **Mentor's rules:** evidence over flattery. If I'm wrong, I get corrected.
  No participation trophies.

## Folder Map
```
.
├── README.md                  ← you are here
├── 00_Curriculum/             ← the master plan (read this first)
│   ├── MASTER_CURRICULUM.md    ← phases, weekly cadence, the whole roadmap
│   ├── PAPER_SEQUENCE.md       ← research papers in pedagogical order + why
│   ├── MATH_PRIMER.md          ← just-in-time math track
│   ├── PYTHON_CORE_TRACK.md    ← Python internals roadmap
│   └── PROGRESS_LOG.md         ← daily log (I fill this in; Hedwig audits it)
├── Chapter01/                 ← book notebooks (Ch.1 Intro to Language Models)
├── 01_GenAI/                  ← my notes / paper summaries / experiments
│   ├── notes/  papers/  code/
├── 02_Python/                 ← Python core track
│   ├── notes/  code/  experiments/   (id, gc, sys, dis probes)
├── 03_ML/                     ← placeholder
├── 04_DL/                     ← placeholder
├── resources/                 ← cheatsheets, links, references
├── environment.yaml           ← book conda env
└── requirements.txt           ← book deps
```

## Start Here
1. Read `00_Curriculum/MASTER_CURRICULUM.md`.
2. Skim `00_Curriculum/PAPER_SEQUENCE.md` so you see the destination.
3. Ask Hedwig: *"What's today's lesson?"* — and we begin.
