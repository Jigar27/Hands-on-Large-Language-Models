# Python Core Track — Becoming Dangerous

**Goal (your words):** understand Python *from the core* — the object model,
the memory model, what actually happens when you create a list or any object,
so you become "a smart coder no one can match."

**Spine:** *Fluent Python* (Ramalho, 2nd ed). **Depth:** CPython-internals
experiments you run yourself. Reading about `id()` teaches you nothing;
*watching two names share one `id()`* rewires your brain.

**Cadence:** 15–20 min/day (the "strength training" block). Every concept ends
with an **experiment in `02_Python/experiments/`** — no passive reading.

---

## Your three power tools (we use these constantly)
- **`id(obj)`** — the object's identity (its address in CPython). Reveals sharing/aliasing.
- **`sys.getsizeof(obj)`** / **`sys.getrefcount(obj)`** — memory footprint & reference counts.
- **`dis.dis(func)`** — disassemble to bytecode. See what the interpreter *actually does*.
- (Later) **`gc`** module, `ctypes`, `tracemalloc`, `timeit`.

---

## Module 1 — The object model (the foundation)
- **Everything is an object.** Identity vs type vs value. `is` vs `==`.
- **Names are not boxes, they're labels.** Variables are references to objects.
- **Experiment:** show that `a = [1,2,3]; b = a` makes `id(a) == id(b)`; mutate through `b`, watch `a` change. Then `b = a[:]` (copy) and watch them diverge.
- **Integer/string interning:** why `a = 256; b = 256; a is b` is `True` but `257` may not be. Why `"hi" is "hi"` but a built string may not.
- **Fluent Python:** Ch.1 (Python Data Model) — the dunder methods that make objects "Pythonic."

## Module 2 — Mutability & memory
- Mutable vs immutable; why this is the #1 source of subtle bugs.
- The classic trap: mutable default arguments (`def f(x, acc=[])`). We'll reproduce the bug, then explain it via the object model.
- Shallow vs deep copy (`copy` module).
- **Reference counting + garbage collection:** `sys.getrefcount`, reference cycles, the `gc` module. CPython = refcounting + a cycle collector.

## Module 3 — How the built-in containers actually work
- **list:** a *dynamic array* of pointers — over-allocation/growth strategy (why `append` is amortized O(1)). Measure growth with `sys.getsizeof`.
- **dict & set:** *hash tables* — hashing, collisions, why keys must be hashable, insertion-order preservation (3.7+), the compact-dict layout.
- **tuple vs list:** why tuples are cheaper/immutable; tuple as a record.
- **Fluent Python:** Ch.2 (Sequences), Ch.3 (Dicts & Sets).

## Module 4 — Functions, scope, closures
- First-class functions; functions as objects.
- Scope rules (LEGB), `global`/`nonlocal`.
- **Closures** and how they capture variables (by reference, not value — another classic gotcha).
- **Fluent Python:** Ch.7 (Functions as first-class objects).

## Module 5 — The data model in depth (dunder methods)
- `__repr__`/`__str__`, `__eq__`/`__hash__`, `__len__`, `__getitem__`, `__iter__`.
- Build a custom class that behaves like a built-in (e.g., a Vector).
- **Fluent Python:** Ch.1 + Ch.11–13 (interfaces, itance, operator overloading).

## Module 6 — Iterators, generators, lazy evaluation
- Iterator protocol (`__iter__`/`__next__`), generators (`yield`), generator expressions.
- Why generators save memory (lazy); `itertools`.
- **Fluent Python:** Ch.17.

## Module 7 — Decorators & the runtime
- Closures → decorators; `functools.wraps`; parametrized decorators.
- **Fluent Python:** Ch.9 (Decorators & Closures).

## Module 8 — Bytecode, the interpreter & the GIL
- `dis` deep dive: see comprehensions vs loops, LOAD_FAST vs LOAD_GLOBAL.
- The **GIL** — what it is, why it exists (CPython refcounting safety), what it means for threads vs processes vs async.
- CPython execution model overview (compile → bytecode → eval loop).

## Module 9 — Performance & memory profiling
- `timeit`, `tracemalloc`, `__slots__` (cutting per-instance memory), interning tricks.
- When to reach for NumPy/arrays vs Python lists (ties straight into the GenAI track).

---

## The "no one can match" standard
A smart Python coder isn't the one who memorizes syntax — it's the one who can
**predict the interpreter's behavior** and **explain *why*.** Every module ends
with you predicting an output *before* running it. A wrong prediction is the
most valuable kind of learning. I'll keep score (kindly-ish).
