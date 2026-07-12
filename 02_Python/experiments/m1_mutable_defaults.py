"""
Python Core - Module 1 (cont.): the mutable default argument trap.

The famous gotcha: a default value like `bag=[]` is evaluated ONCE, at
function-DEFINITION time, and stored on the function object. Every call that
omits the argument reuses that SAME list -> state leaks between calls.
This is just Day-1 aliasing wearing a disguise.

Predict each print BEFORE running. Reality is the grader.
Run:  python 02_Python/experiments/m1_mutable_defaults.py
"""

print("=== 1. The trap: bag=[] is created ONCE, at def time, and shared ===")


def add_item(item, bag=[]):        # DANGER: mutable default
    bag.append(item)
    return bag


print("add_item('apple')  ->", add_item("apple"))    # ['apple']
print("add_item('banana') ->", add_item("banana"))   # ['apple', 'banana']  <- leaked!
print("add_item('cherry') ->", add_item("cherry"))   # ['apple', 'banana', 'cherry']

# The smoking gun: the default list lives ON the function object and
# carries state BETWEEN calls. There is only ONE list, born when `def` ran.
print("stored default:", add_item.__defaults__)      # (['apple','banana','cherry'],)
print("id of default :", id(add_item.__defaults__[0]))

print("\n=== 2. Why: the default is evaluated at DEFINITION time (once) ===")


def make_fn():
    print("  (evaluating the default [] right now, as `def` runs)")

    def fn(x, bag=[]):             # this [] is built once, when make_fn() defines fn
        bag.append(x)
        return bag
    return fn


f = make_fn()                      # <- the default [] is created HERE, not on each call
print("f(1) ->", f(1))             # [1]
print("f(2) ->", f(2))             # [1, 2]  <- same shared list

print("\n=== 3. The fix: use None as an immutable sentinel ===")


def add_item_safe(item, bag=None):
    if bag is None:                # 'is' is correct here: None is a singleton
        bag = []                   # fresh list created on THIS call, in the body
    bag.append(item)
    return bag


print("add_item_safe('apple')  ->", add_item_safe("apple"))    # ['apple']
print("add_item_safe('banana') ->", add_item_safe("banana"))   # ['banana']  <- fresh!
print("add_item_safe('cherry') ->", add_item_safe("cherry"))   # ['cherry']
print("stored default:", add_item_safe.__defaults__)           # (None,) -> nothing leaks

print("\n=== 4. The rule ===")
print("Never use a mutable default (list/dict/set). Default to None,")
print("then build the mutable object inside the function body.")
