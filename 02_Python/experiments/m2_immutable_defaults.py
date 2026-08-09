"""
Day 3 warm-up (Jigar's question from Day 2 debrief):
1) Is an immutable default (like None) ALSO created once and stored on the
   function object, same as a mutable default?
2) Would ANY immutable default fix the mutable-default trap, not just None?

Answer to both, with receipts:
1) Yes -- every default, mutable or immutable, is evaluated ONCE at def time
   and stored in func.__defaults__. None gets no special treatment there.
2) Partially. Immutability kills the ACCUMULATION bug (nothing can mutate
   in place). But it doesn't automatically make a value a good SENTINEL
   ("caller passed nothing"). That needs a value no real caller would ever
   pass on purpose -- which is exactly what None is for.
"""


def add_item_mutable(item, bag=[]):
    bag.append(item)          # mutates the SAME list object every call
    return bag


def add_item_immutable_tuple(item, bag=()):
    bag = bag + (item,)       # tuples are immutable -> this REBINDS bag to a
    return bag                # brand-new tuple; the original default is untouched


def add_item_none_sentinel(item, bag=None):
    if bag is None:
        bag = []              # fresh list built in the function BODY, each call
    bag.append(item)
    return bag


print("=== Experiment 1: what's sitting in func.__defaults__ right after def? ===")
print("mutable default (list) :", add_item_mutable.__defaults__)
print("immutable default (tup):", add_item_immutable_tuple.__defaults__)
print("None default           :", add_item_none_sentinel.__defaults__)
print("-> ALL THREE store something at definition time. None isn't special-cased")
print("   here -- it's just a reference to the one singleton None object.\n")

print("=== Experiment 2: does the accumulation bug survive with an immutable default? ===")
print("mutable list version:")
print(" ", add_item_mutable("apple"))
print(" ", add_item_mutable("banana"))   # BUG: same list keeps growing
print("immutable tuple version:")
print(" ", add_item_immutable_tuple("apple"))
print(" ", add_item_immutable_tuple("banana"))  # fixed: fresh tuple every call
print("-> tuple default never changes:", add_item_immutable_tuple.__defaults__)
print("   '+' on a tuple can't mutate it in place, so it MUST build a new object")
print("   and rebind the local name. The shared default object is never touched.\n")

print("=== Experiment 3: the trap -- immutable is NOT the same as 'good sentinel' ===")


def set_discount_bad(pct=0):     # using 0 to mean 'nothing specified'
    if pct == 0:
        pct = 5                  # 'apply the default 5% discount'
    return pct


print("caller passes nothing      :", set_discount_bad())     # -> 5, looks fine
print("caller explicitly passes 0 :", set_discount_bad(0))    # -> 5, WRONG! wanted 0
print("-> 0 is immutable (no accumulation bug), but it's a BAD sentinel: you can no")
print("   longer tell 'nothing passed' apart from 'caller really meant 0'.\n")


def set_discount_good(pct=None):
    if pct is None:
        pct = 5
    return pct


print("caller passes nothing      :", set_discount_good())
print("caller explicitly passes 0 :", set_discount_good(0))
print("-> None is a good sentinel because it means exactly ONE thing:")
print("   'no argument given'. It's never a value a caller legitimately wants,")
print("   unlike 0, '', [], or False -- all of which ARE valid real inputs.")
