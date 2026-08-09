"""
Day 3 follow-up (Jigar's question): why `is None` and never `== None`?

Short answer: `==` calls the object's __eq__ method, which is CUSTOMIZABLE.
A misbehaving (or just differently-designed) class can make `obj == None`
lie to you. `is` compares raw identity -- it can NEVER be overridden or
fooled. Since None is a singleton, identity comparison is both CORRECT
and the semantically honest question ("is this THE None object?").

Two real demonstrations below.
"""

print("=== Demo 1: a class that overrides __eq__ to always agree ===")


class YesMan:
    """A deliberately unhinged class: says '==' to EVERYTHING, even None."""
    def __eq__(self, other):
        return True   # bad citizen, but 100% legal Python


ym = YesMan()
print("ym == None :", ym == None)   # True  <- WRONG! ym is clearly not None
print("ym is None :", ym is None)   # False <- correct, ym is a YesMan object
print("-> '==' asked YesMan's __eq__ method, which lied. 'is' can't be lied")
print("   to -- it just compares raw object identity (memory address).\n")

print("=== Demo 2: a REAL example from ML work (numpy arrays) ===")
try:
    import numpy as np
    arr = np.array([1, 2, 3])
    print("arr == None ->", arr == None)   # elementwise: array([False, False, False])
    print("   (that's an ARRAY of 3 bools, not one bool!)")
    try:
        if arr == None:
            pass
    except ValueError as e:
        print("   using it in `if arr == None:` blows up ->", e)
    print("arr is None ->", arr is None)   # just: False. Single clean bool.
    print("-> 'is None' is not just style here -- '== None' can be an outright")
    print("   crash risk with numpy/pandas objects that overload '=='.")
except ImportError:
    print("(numpy not installed in this env -- skip, but the YesMan demo above")
    print(" already proves the point structurally.)")

print("\n=== The rule ===")
print("`is` = 'are these the literal SAME object?' -> can't be overridden, can't lie.")
print("`==` = 'do these count as equal?' -> customizable via __eq__, CAN lie.")
print("None is a singleton (exactly one None ever exists) so the honest, safe,")
print("un-fool-able question is always: 'is this THE None?' -> use `is None`.")
