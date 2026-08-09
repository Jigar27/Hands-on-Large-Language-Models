# Day 3 Session Transcript — 2026-08-08

> Interactive record. Summary goes in `PROGRESS_LOG.md` at session end;
> runnable code lives in `02_Python/experiments/` and `01_GenAI/code/`.

---

## Part 0 — Carry-over Q&A from Day 2 debrief (mutable defaults deep-dive)

**Jigar's Q1:** We solved the mutable-default-arg bug with `None` (immutable).
Is an immutable default ALSO created once and stored on the function object,
same as a mutable one? And would ANY immutable object fix the bug the same way?

- **Experiment (`m2_immutable_defaults.py`):** `func.__defaults__` shows a
  tuple built once at `def` time for ALL defaults regardless of mutability --
  `([],)` for a mutable list, `((),)` for an immutable tuple, `(None,)` for
  None. No special-casing of None here.
- **Split the bug in two:**
  - **Accumulation bug:** ANY immutable default fixes this (can't mutate in
    place -> operations like `bag + (item,)` build a new object and rebind).
  - **Sentinel-safety bug (the twist):** immutability alone is NOT enough.
    `pct=0` used as a "nothing passed" sentinel silently overrides a caller who
    genuinely means `0` (`set_discount_bad(0)` wrongly returns 5). `None`
    works because it's a value no real caller ever means as actual data.
- **Conclusion:** immutability solves accumulation; semantic uniqueness
  (sentinel-safety) is a separate property. `None` happens to have both.

**Jigar's Q2:** What even IS a "sentinel"? And why `is None` instead of
`== None`?

- **Sentinel, plain language:** a marker object whose only job is to mean
  "no real value was given here" -- like the flag on a mailbox. Must be a
  value no caller would ever legitimately pass as real data (why `0`/`""`
  make bad sentinels but `None` is good).
- **`is` vs `==` experiment (`m3_is_none_vs_eq_none.py`):** a `YesMan` class
  that overrides `__eq__` to always return `True` makes `ym == None` lie
  (`True`, even though `ym` is clearly not None). `ym is None` correctly says
  `False` and cannot be fooled -- `is` is raw identity comparison, immune to
  any class's custom `__eq__`.
- **Real-world hazard flagged:** `numpy_array == None` returns an elementwise
  array of bools, not one bool, and crashes `if` statements built on it
  (`ValueError: truth value of an array is ambiguous`) -- a live landmine in
  ML code. `arr is None` stays a clean single bool.

**Jigar's follow-up (self-correction moment):** "So `is` is better than `==`,
but it only works because None is a singleton." -- **Corrected:**

- **Experiment (`m4_is_vs_eq_general_rule.py`):** two equal-but-distinct lists
  `a=[1,2,3]` and `b=[1,2,3]` give `a == b -> True` but `a is b -> False`. If
  `is` were "generally better," this would be a bug -- it isn't, because `is`
  correctly answered a DIFFERENT question ("same object?") than the one
  Jigar actually wanted ("same value?").
- **Reframed rule:** `is` and `==` ask different questions; they only agree
  when identity and equality collapse into the same thing, which happens
  ONLY for singletons (`None`, `True`, `False`). For everything else
  (numbers, strings, lists, custom objects), `==` is the correct tool.
- **Final rule banked:** `is` for singleton checks (`None`/`True`/`False`);
  `==` for value comparisons everywhere else. Not a hierarchy of "better" --
  a matter of which question you're actually asking.

**New glossary terms added:** Singleton, Sentinel value.

---

## Part 1 — Day 3 main lesson (in progress)

