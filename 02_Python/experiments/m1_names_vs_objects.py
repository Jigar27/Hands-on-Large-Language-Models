"""
Python Core — Module 1: names are labels, not boxes.

Predict each print BEFORE running. Reality is the grader.
Run:  python 02_Python/experiments/m1_names_vs_objects.py
"""

print("=== 1. Aliasing: b = a makes a SECOND sticky-note, not a copy ===")
a = [1, 2, 3]
b = a                 # b points at the SAME list object as a
b.append(4)
print("a         =", a)              # [1, 2, 3, 4]  <- a changed too!
print("b         =", b)              # [1, 2, 3, 4]
print(f'Id(a) = {id(a)}')
print(f'Id(b) = {id(b)}')
print("id(a)==id(b)?", id(a) == id(b))   # True: one object, two names

print("\n=== 2. The fix: b = a[:] makes a real COPY (new object) ===")
a = [1, 2, 3]
b = a[:]              # slice copy -> brand-new list object
b.append(4)
print("a         =", a)              # [1, 2, 3]     <- untouched!
print("b         =", b)              # [1, 2, 3, 4]
print(f'Id(a) = {id(a)}')
print(f'Id(b) = {id(b)}')
print("id(a)==id(b)?", id(a) == id(b))   # False: two separate objects

print("\n=== 4. Constant Folding ===")
a = [1, 2, 3]
b = [1, 2, 3]
print(f'Id(a) = {id(a)}')
print(f'Id(b) = {id(b)}')
print("a is b ?", a is b)

print("\n=== 3. Integer interning: small ints are pre-made & shared ===")
x = 256
y = 256
print(f'Id(x) = {id(x)}')
print(f'Id(y) = {id(y)}')

x = 256
y = int("256")
print(f'Id(x) = {id(x)}')
print(f'Id(y) = {id(y)}')

print("256 is 256 ?", x is y)        # True: CPython caches -5..256
p = 257
q = 257
print(f'Id(p) = {id(p)}')
print(f'Id(q) = {id(q)}')

p = 257
q = int("257")
print(f'Id(p) = {id(p)}')
print(f'Id(q) = {id(q)}')

print("257 is 257 ?", p is q)        # often False: not cached (may vary)
