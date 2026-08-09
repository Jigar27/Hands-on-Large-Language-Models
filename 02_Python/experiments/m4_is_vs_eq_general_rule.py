"""
Day 3 follow-up #2: is `is` just BETTER than `==`? No -- they answer
DIFFERENT questions. `is` only gives the answer you WANT when identity and
equality happen to mean the same thing -- which is exactly the case for a
singleton like None, and exactly NOT the case for ordinary objects.
"""

print("=== Demo: `is` is NOT generally 'better' -- watch it give a 'wrong' answer ===")
a = [1, 2, 3]
b = [1, 2, 3]
print("a =", a, " b =", b)
print("a == b :", a == b)   # True -- same VALUE
print("a is b :", a is b)   # False -- different OBJECTS in memory
print("-> If 'is' were universally better, this would be a bug. It's not a bug --")
print("   'is' correctly answered 'are these the same object?' (no). It just")
print("   wasn't the question you actually cared about here (you wanted VALUE).\n")

print("=== Why None is different: singleton collapses the two questions into one ===")
x = None
y = None
print("x is y :", x is y)    # True -- there is only EVER one None object
print("x == y :", x == y)    # True -- also true, same value
print("-> Because there's only EVER one None in the whole program, 'same object")
print("   as None' and 'equal to None' become the SAME question. That's the only")
print("   reason `is None` is safe AND correct -- not because `is` is superior.\n")

print("=== The actual rule (not 'is > ==', but 'right tool for the question') ===")
print("- Asking 'is this THE None / True / False?'      -> use `is`  (singletons)")
print("- Asking 'do these two things have the same value?' -> use `==` (everything else:")
print("  ints, strings, lists, dicts, your own classes)")
