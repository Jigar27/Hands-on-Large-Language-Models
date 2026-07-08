# Glossary — Terms Hedwig Drops Along the Way

> A running list. Whenever Hedwig uses a term (tech, math, ML, Japanese loan
> words, whatever), it lands here so it never just evaporates. Re-read often.
> Newest sections get appended; keep it alphabetical-ish within a category.

## Culture / learning
- **Dojo** (Japanese, "place of the way") - a martial-arts training hall where
  you show up regularly, drill fundamentals, and get corrected by a sensei. In
  tech, a "coding dojo" = a deliberate-practice space. Here it means your
  `Self_Study` repo.
- **Sensei** - teacher/master in a dojo. (That's Hedwig's role: the slightly
  too-harsh one who makes you redo the kata.)
- **Kata** - a choreographed practice routine in martial arts; in coding, a
  small exercise you repeat to build fluency.
- **Feynman technique** - learn by explaining a concept in plain language as if
  teaching a beginner; the gaps you stumble on reveal what you don't really know.

## Git / GitHub
- **Git** - the version-control tool that runs locally on your laptop.
- **GitHub** - a website that hosts copies of Git repos (one of several; others:
  GitLab, Bitbucket).
- **Repo (repository)** - a project tracked by Git (the folder + its `.git/` history).
- **Commit** - a permanent labeled snapshot of your staged changes.
- **Staging area (index)** - the "on-deck" list of changes that will go in the
  next commit.
- **origin** - conventional nickname for your main remote (a bookmark to a URL).
- **Upstream / tracking branch** - the link between local `main` and
  `origin/main`; shown as `[origin/main]` in `git branch -vv`. Set via `git push -u`.
- **Commit hash** - the unique id of a snapshot (e.g. `3502783`).
- **HEAD** - pointer to your current commit/branch.
- **SSH key** - a cryptographic keypair used to authenticate to GitHub. Private
  half stays secret on your laptop; public half is pasted into GitHub. NOT tied
  to any email (the comment in the `.pub` file is cosmetic).
- **PAT (Personal Access Token)** - a token used as a password substitute for
  HTTPS git auth (GitHub killed plain passwords in 2021).

## GenAI / ML (seeded; grows as we go)
- **Embedding** - a dense vector of numbers representing a word/token/item, where
  geometric closeness ~ semantic similarity.
- **Token** - the unit an LLM actually reads (a word, sub-word, or character chunk).
- **Dot product** - a single number measuring how much two vectors point the
  same direction; the building block of similarity and attention.
- **Cosine similarity** - dot product normalized by vector lengths; a similarity
  score in [-1, 1].
- **Softmax** - turns a list of raw scores into probabilities that sum to 1 (a
  "spotlight" that brightens the largest scores).
- **Vector** - a list of numbers; equivalently an arrow / a point in space. An
  embedding is a vector.
- **Dimension** - how many numbers are in a vector. `[3,4]` = 2-D; GPT embeddings
  are often 768- or 1536-D. Each dimension is one learned axis of meaning.
- **Magnitude (length)** of a vector - `sqrt(sum of squares)`; Pythagoras generalized.
- **Orthogonal** - the math word for perpendicular: dot product = 0, 90 deg apart.
- **arccos (inverse cosine)** - runs cosine backwards: give it a cosine value, it
  returns the angle. `arccos(0.8) ~= 37 deg`.
- **Nearest-neighbor search** - given a query vector, scan a set and return the
  most cosine-similar one(s). The mechanism under semantic search and RAG retrieval.

## Statistics / sampling / causal inference (grows as we go)
> Seeded 2026-07-06, motivated by a real problem on the **VELMA** project
> (a decision layer over Sam's Club Exit ML + Exit CV checkout audits). See the
> worked example in `03_ML/notes/covariate_balance_and_missingness.md`.

- **Covariate** - any measured feature/variable that describes a unit but isn't
  the outcome you're studying. In VELMA: basket size, club, hour-of-day, risk
  decile, CV coverage band. ("Co-" = alongside; it varies *alongside* the thing
  you actually care about.)
- **Covariate distribution** - the *shape* of how a covariate is spread across a
  group: its histogram/density (e.g., "what fraction of audited baskets fall in
  each risk decile"). Not one number — the whole spread.
- **Balance check** - comparing the covariate distributions of two groups
  feature-by-feature to see if they *look the same*. If group A (leaked/audited
  1%) and group B (full population) have matching distributions on every
  covariate, the sample is "balanced" / representative. Imbalance = red flag.
- **Representative sample** - a subset whose covariate distributions match the
  population it's drawn from, so estimates on the subset generalize.
- **Selection bias** - systematic error from *how units got into your sample*.
  If the reason a basket landed in the audited 1% is correlated with its risk,
  your fail-rate estimate is biased. ("Who got measured" is not random.)
- **Natural experiment** - a situation where some outside quirk (here: network
  *latency* dropping ~1% of CV recommendations) splits units into groups *as if*
  randomized — letting you estimate effects without running a real experiment.
  Only trustworthy if the quirk is independent of the outcome/risk.
- **Missingness taxonomy (Rubin)** - a classification of *why* data is missing:
  - **MCAR (Missing Completely At Random)** - missingness is independent of
    everything (observed *and* unobserved). The dropped baskets are a random
    coin-flip. This is the golden assumption: the observed subset is an unbiased
    mini-me of the whole. *VELMA needs this to be true.*
  - **MAR (Missing At Random)** - missingness depends only on *observed*
    covariates (e.g., latency drops more at busy clubs, but you *recorded* club
    traffic). Fixable by conditioning/weighting on those covariates.
  - **MNAR (Missing Not At Random)** - missingness depends on the *unobserved*
    value itself (e.g., riskier baskets are somehow more likely to be dropped
    for reasons you can't measure). The nightmare: not fixable from the data
    alone; estimates stay biased.
- **Covariate shift** - the *inputs'* distribution changes between two settings
  (train vs. deploy, or subset vs. population) while the input→output
  relationship P(y|x) stays the same. Contrast with **selection bias**, which is
  about *how the sample was selected*; covariate shift is about the *feature
  distribution differing*. They overlap but aren't identical — see the note.
- **SMD (Standardized Mean Difference)** - a scale-free measure of how far apart
  two groups' means are for a covariate: (mean_A − mean_B) / pooled_SD. Rule of
  thumb: |SMD| < 0.1 ≈ balanced. Cheap first-pass balance diagnostic; only
  catches *mean* differences, not shape.
- **KS test (Kolmogorov–Smirnov, two-sample)** - a test comparing two full
  distributions by their largest gap between cumulative distribution functions
  (CDFs). Catches shape differences SMD misses, but with huge N it flags
  trivially-tiny differences as "significant" (statistical ≠ practical).
- **CDF (Cumulative Distribution Function)** - F(x) = P(value ≤ x); the running
  total of a distribution from left to right, going 0 → 1.
- **p-value** - probability of seeing data this extreme (or more) *if* the null
  hypothesis were true. Small p = data is surprising under the null. NOT the
  probability the null is true, and NOT an effect size.

## Python internals (seeded; grows as we go)
- **Object model** - Python's rule that *everything* is an object with an
  identity, a type, and a value.
- **Identity (`id()`)** - a unique number for an object (its address in CPython);
  `is` compares identity, `==` compares value.
- **Reference / name** - a variable is a label pointing at an object, not a box
  holding it.
- **Mutable vs immutable** - whether an object's value can change in place
  (list/dict = mutable; int/str/tuple = immutable).
- **Aliasing** - two names pointing at the SAME object (`b = a`). Mutating through
  one is visible through the other. `b = a[:]` makes a real copy (new object).
- **`is` vs `==`** - `is` compares identity (same object?), `==` compares value.
  RULE: use `==` for values; reserve `is` for `None`/`True`/`False`.
- **Interning** - reusing one shared object for repeated values. CPython caches
  small ints (-5..256) and some short strings.
- **Constant folding** - compile-time optimization: the compiler dedupes/precomputes
  literal constants within a single code object (why `257 is 257` can be True in a
  script but False across separate REPL lines).
