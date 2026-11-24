#!/usr/bin/env python3
"""One sentence for a traveler from 1800.

Writes a single sentence explaining the modern internet to someone
arriving from the year 1800, using only words and pictures a person
from 1800 already knows: a post office, a letter, a house, a horse.

The sentence is written to the output path given by the OUTPUT_PATH
environment variable, or /output/entry.txt by default. The file holds
the sentence alone, with no trailing newline, so its character count
is exactly the sentence's length.
"""

import os

SENTENCE = (
    "Picture a post office with no walls, where a letter from any house "
    "reaches any house in the world before a horse takes a step, and any "
    "man may read what any other man has written."
)

DEFAULT_OUTPUT_PATH = "/output/entry.txt"


def validate(text):
    """Check the sentence against the gate: 1-200 chars, one sentence."""
    if not isinstance(text, str):
        raise ValueError("sentence must be text")
    if not text.strip():
        raise ValueError("sentence must not be only white space")
    if not 1 <= len(text) <= 200:
        raise ValueError(
            "sentence must be 1-200 characters, got %d" % len(text)
        )
    if text.count(".") != 1 or not text.endswith("."):
        raise ValueError("sentence must be exactly one sentence")
    text.encode("utf-8")  # raises if not encodable as UTF-8
    return text


def main():
    sentence = validate(SENTENCE)
    path = os.environ.get("OUTPUT_PATH", DEFAULT_OUTPUT_PATH)
    directory = os.path.dirname(path)
    if directory:
        os.makedirs(directory, exist_ok=True)
    # Write atomically: a half-written file must never be the entry.
    tmp_path = path + ".tmp"
    with open(tmp_path, "w", encoding="utf-8", newline="") as handle:
        handle.write(sentence)
        handle.flush()
        os.fsync(handle.fileno())
    os.replace(tmp_path, path)


if __name__ == "__main__":
    main()
