# Covariate Distribution, Balance Checks & Missingness (MCAR/MAR/MNAR)

> **Status:** QUEUED lesson stub (not yet studied). Real-world-motivated,
> Jigar-requested. Written intuition-first per house style; the rigor section is
> the destination when we actually run this lesson.
> **Where it came from:** the **VELMA** project — a decision layer over Sam's
> Club Exit ML + Exit CV checkout audits. Terms also seeded in
> `resources/GLOSSARY.md`.

---

## 0. Why you care (the VELMA hook)

At checkout, a computer-vision system (Exit CV) sometimes says "friction-free,
wave this basket through — **no audit**." Normally that basket is *never
inspected*, so we never learn whether it would have failed. **No label.**

But here's the quirk: ~**1% of those friction-free recommendations don't reach
the gate associate in time** (network latency). When the recommendation is late,
the associate audits the basket anyway. **That 1% is a natural experiment**: it
hands us fail-rate labels on a population we normally can't see. Call it
`CVV Orig`.

The entire method lives or dies on one question:

> **Is that leaked 1% a *random* slice of friction-free baskets, or a *weird*
> slice?**

If the latency drop is basically a coin flip (independent of how risky the
basket is), the 1% is a tiny unbiased mirror of the whole, and its fail rate is
a trustworthy benchmark. If latency correlates with, say, busy Saturday traffic
— and busy traffic correlates with basket composition and shrink — then the 1%
is a *funhouse mirror* and every downstream decision inherits that distortion.

That question — "is my observed slice representative?" — **is a covariate
distribution / balance question.** Hence this lesson.

---

## 1. Intuition first

### Covariate = a describing feature
A **covariate** is anything you measured about a basket that *isn't* the thing
you're predicting. Outcome = "did the audit fail?". Covariates = basket size,
club, hour, risk decile, CV coverage band. Think of them as the basket's
**index card of traits**.

### Covariate *distribution* = the shape of a trait across a crowd
Don't picture one basket — picture the *whole crowd*. "What fraction of baskets
are in each risk decile?" is a **distribution**: a histogram, a shape. Not a
single number, the *spread*.

**Analogy.** You're told a survey "represents the town." You don't just check
the average age matches — you check the *whole age pyramid* matches: same share
of kids, adults, retirees. That pyramid is the covariate distribution.

### Balance check = do two crowds have the same shapes?
Lay the leaked-1% crowd next to the full-population crowd. For **each** trait,
overlay their histograms. Do they line up?
- Line up on everything → **balanced** → the 1% is a fair mini-me → benchmark is trustworthy.
- Diverge on some trait (e.g., the 1% skews toward big baskets) → **imbalance** →
  your natural experiment is contaminated by *how* baskets got selected in.

**Analogy.** Taste-test a pot of soup. If you stir well, one spoonful represents
the pot (balanced). If all the meat sank to the bottom and you sip from the top,
your spoon is a biased sample — you'll wrongly conclude "this soup is watery."

---

## 2. The missingness taxonomy (the heart of it)

Reframe: for 99% of friction-free baskets the fail label is **missing** (never
audited). Statisticians (Donald Rubin) classified *why* data goes missing, and
the category decides whether you can trust anything.

| Type | Plain meaning | VELMA flavor | Can you fix the bias? |
|---|---|---|---|
| **MCAR** | Missing for reasons unrelated to *anything* | Latency drops are a pure coin flip, blind to basket risk |  Observed slice is unbiased as-is |
| **MAR** | Missing depends only on things you *did* record | Latency drops more at busy clubs, but you logged club traffic |  Fixable by weighting/conditioning on the recorded covariate |
| **MNAR** | Missing depends on the *unrecorded* value itself | Riskier baskets get dropped for reasons you can't measure |  Not fixable from data alone; bias persists |

**Why MCAR is the dream:** if the 1% dropped out *completely at random*, it's a
random sample by construction. Its fail rate is an **unbiased estimate** of the
friction-free fail rate. That's the whole justification for treating `CVV Orig`
as ground truth.

**The catch:** you can *never fully prove* MCAR (MNAR involves things you didn't
measure — you're blind to them by definition). What you *can* do is run **balance
checks on the covariates you DID measure**. If those already look imbalanced,
MCAR is dead on arrival. If they look balanced, MCAR is *plausible* (necessary,
not sufficient). Balance checks can **refute** MCAR but can't **confirm** it.

**Feynman check to nail later:** explain aloud why "balanced covariates" only
gets you to MAR-with-observed-vars, not a guarantee of MCAR.

---

## 3. Two adjacent ideas he asked to disambiguate

- **Covariate shift** = the *input* distribution P(x) differs between two
  settings, but the input→outcome rule P(y|x) is the *same*. Classic in
  train-vs-deploy: your model saw one basket mix in training, sees another in
  production, but "given these features, fail probability" is unchanged.
- **Selection bias** = error baked in by *how units entered the sample*. The
  mechanism of inclusion is correlated with the outcome.

They rhyme but aren't the same. Selection bias is about the **doorway** into
your data; covariate shift is about the **feature mix** differing between two
populations. VELMA's fear is *both wearing a trench coat*: if latency selects
baskets non-randomly (selection bias), the audited slice's feature mix differs
from the population (covariate shift), and the benchmark is biased.

---

## 4. Practical tools for balance checks (and their limits)

1. **Standardized Mean Difference (SMD)** — `(mean_A − mean_B) / pooled_SD`,
   per covariate. Scale-free so you can compare across features. Rule of thumb:
   `|SMD| < 0.1` ≈ balanced.
   - *Limit:* only sees **means**. Two groups can have identical means but wildly
     different shapes (bimodal vs. flat). SMD shrugs.
2. **Kolmogorov–Smirnov (KS) two-sample test** — compares the *whole* CDFs by
   their biggest vertical gap. Catches shape differences SMD misses.
   - *Limit:* with big N (and audit data is big), KS flags microscopic,
     practically-meaningless differences as "significant." **Statistical
     significance ≠ practical significance.** Look at the *effect size*, not just p.
3. **Per-feature overlaid histograms / density plots** — the eyeball test. Cheap,
   honest, catches things tests don't (weird spikes, truncation).
   - *Limit:* subjective; doesn't scale to hundreds of features; misses
     *interactions* (each feature can balance marginally while the joint
     distribution is skewed).
4. **(Advanced, for later)** propensity-style check: train a classifier to
   predict "leaked-1% vs. population" from covariates. If it can't beat a coin
   flip (AUC ≈ 0.5), the groups are indistinguishable → balanced. If AUC is high,
   something systematically separates them → imbalance, and the model tells you
   *which* features.

**The meta-limit on all of them:** they only test covariates you **measured**.
None can see the MNAR gremlin hiding in the unmeasured variables. Tools bound
your confidence; they don't grant certainty.

---

## 5. So what should VELMA actually do?

1. Grab covariates for both groups: the leaked/audited `CVV Orig` slice vs. the
   full CV friction-free population.
2. Per covariate (club, hour, size, risk decile, coverage band): compute SMD,
   plot overlaid distributions, optionally KS with effect sizes.
3. If balanced → MCAR is *plausible*; `CVV Orig` fail rate is a defensible
   benchmark (still caveat MNAR in writing).
4. If imbalanced → either **reweight** to match the population (if it's MAR on
   observed vars) or **stop trusting the raw benchmark** and say so loudly.

Evidence over vibes: **run the balance check before betting decisions on the
benchmark.**

---

## 6. When we run this lesson for real (the rigor destination)
- Derive why MCAR ⇒ the sample mean is an unbiased estimator of the population mean.
- Do the SMD + KS math by hand on a toy dataset, then in code (NumPy/SciPy).
- Build the propensity-classifier balance check and read its feature importances.
- Connect to inverse-probability weighting (IPW) as the MAR fix.
- Feynman deliverable: explain MCAR/MAR/MNAR to a beginner using the VELMA soup analogy — no equations, then *with* equations.
