# 03 ML — Placeholder

Objectives to be defined by Jigar. Structure will mirror the GenAI track:
notes / code / curated paper sequence / just-in-time math.

NOTE (Hedwig): much of "classical ML theory" you already apply at work
(XGBoost/LightGBM, thresholds, feature engineering). When we build this track
we'll focus on the *gaps* (the math/theory behind what you already do) rather
than re-teaching what you practice daily. DRY applies to curricula too.

---

## Queued topics (Jigar-requested, real-world-motivated)

These jump the line because they came from an *actual* problem at work, not a
textbook TOC. That's the best kind of lesson — you already have the motivation.

- **Covariate distribution & balance checks / missingness (MCAR/MAR/MNAR)**
  — QUEUED 2026-07-06. Motivated by the **VELMA** project (decision layer over
  Sam's Club Exit ML + Exit CV audits): a ~1% latency "leak" gives fail labels
  on normally-unaudited baskets, and the method's validity hinges on whether
  that leaked slice is *representative*. Covers: covariates & their
  distributions, balance checks, the MCAR/MAR/MNAR taxonomy, covariate shift
  vs. selection bias, and practical tools (SMD, KS test, distribution plots,
  propensity check) + their limits.
  Intuition-first stub already written: [`notes/covariate_balance_and_missingness.md`](notes/covariate_balance_and_missingness.md).
  Glossary terms seeded in `resources/GLOSSARY.md`.
