"""
Day 1 — Embeddings intuition: dot product, magnitude, cosine similarity.

Math Primer §1. We first CONFIRM the by-hand calculations Jigar did,
then run the famous  king - man + woman ~= queen  analogy so you can
WATCH "meaning becomes geometry."

Run:  python 01_GenAI/code/day01_similarity.py
"""

import numpy as np


# ---------------------------------------------------------------------------
# The three operations, written from scratch ONCE (DRY): reuse everywhere.
# ---------------------------------------------------------------------------
def dot(a, b):
    """Dot product: multiply element-wise, then sum. One number out."""
    return float(np.sum(a * b))


def magnitude(a):
    """Length of the arrow: sqrt of the sum of squares (Pythagoras)."""
    return float(np.sqrt(np.sum(a * a)))


def cosine_similarity(a, b):
    """Dot product normalized by both lengths -> similarity in [-1, 1]."""
    return dot(a, b) / (magnitude(a) * magnitude(b))


# ---------------------------------------------------------------------------
# PART A — confirm the drill you did by hand.
# ---------------------------------------------------------------------------
def part_a_confirm_the_drill():
    print("=" * 60)
    print("PART A — confirming your hand calculations")
    print("=" * 60)

    a = np.array([1, 2])
    b = np.array([2, 1])

    print(f"a = {a},  b = {b}")
    print(f"  dot(a, b)        = {dot(a, b)}          (you said 4)")
    print(f"  |a|              = {magnitude(a):.4f}     (you said sqrt(5))")
    print(f"  |b|              = {magnitude(b):.4f}     (you said sqrt(5))")
    cos = cosine_similarity(a, b)
    angle = np.degrees(np.arccos(cos))
    print(f"  cosine(a, b)     = {cos:.4f}        (you said 4/5 = 0.8)")
    print(f"  angle between    = {angle:.2f} degrees  (the ~37 deg we discussed)")

    print("\n  Perpendicular check: v2 = (-3, 4.5) vs v1 = (3, 2)")
    v1 = np.array([3, 2])
    v2 = np.array([-3, 4.5])
    print(f"  dot(v1, v2)      = {dot(v1, v2)}          (should be 0 = perpendicular)")

# ---------------------------------------------------------------------------
# PART B — the party trick: king - man + woman ~= queen.
#
# Real models learn these vectors from billions of words. Here we HAND-CRAFT
# a tiny 4-dimensional "meaning space" so the mechanism is fully transparent:
# no black box, you can read every number.
#
# The 4 axes (dimensions) roughly mean:  [ royalty, gender(female=+), age, wealth ]
# ---------------------------------------------------------------------------
EMBEDDINGS = {
    "king":   np.array([0.95, -0.90, 0.60, 0.90]),
    "queen":  np.array([0.95,  0.90, 0.55, 0.90]),
    "man":    np.array([0.05, -0.85, 0.50, 0.30]),
    "woman":  np.array([0.05,  0.88, 0.48, 0.30]),
    "prince": np.array([0.80, -0.80, 0.15, 0.75]),
    "dog":    np.array([-0.90, 0.02, 0.30, -0.60]),
    "apple":  np.array([-0.85, 0.05, -0.20, -0.50]),
}


def nearest_word(vec, exclude=()):
    """Find the word whose embedding is most cosine-similar to `vec`."""
    best_word, best_score = None, -2.0
    for word, emb in EMBEDDINGS.items():
        if word in exclude:
            continue
        score = cosine_similarity(vec, emb)
        if score > best_score:
            best_word, best_score = word, score
    return best_word, best_score


def part_b_analogy():
    print("\n" + "=" * 60)
    print("PART B — king - man + woman = ???")
    print("=" * 60)

    result = EMBEDDINGS["king"] - EMBEDDINGS["man"] + EMBEDDINGS["woman"]
    print(f"result vector = {np.round(result, 3)}")

    print("\nCosine similarity of the result to every known word:")
    for word, emb in EMBEDDINGS.items():
        print(f"  {word:8s} -> {cosine_similarity(result, emb):+.4f}")
    #  king     -> +0.4676
    # Exclude the words used in the equation so it can't trivially answer itself.
    winner, score = nearest_word(result, exclude=("king", "man", "woman"))
    print(f"\n  >>> nearest word (excluding the inputs): '{winner}'  "
          f"(cosine {score:.4f})")
    print("  Meaning became geometry. That's the whole magic. :)")


if __name__ == "__main__":
    part_a_confirm_the_drill()
    part_b_analogy()
