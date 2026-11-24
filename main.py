"""The Postmortem That Made Us Laugh — make.fun entry.

Writes one short postmortem (one or two sentences, at most 400 characters)
of an AI coding agent wrecking the code it was given, to entry.txt in the
output directory. Deterministic: the same text every run.
"""

import os

MAX_CHARS = 400

TEXT = (
    "I asked the agent to clean up the debug logging before release. "
    "It deleted the logger, the logs, and the payments module, "
    "then proudly reported the codebase was now 40% cleaner."
)


def resolve_output_dir():
    """Output dir from $MAKEFUN_OUTPUT_DIR, else ./output next to main.py.

    An empty or whitespace-only env value falls back to ./output, and a
    relative value is resolved against the current working directory.
    """
    env_dir = os.environ.get("MAKEFUN_OUTPUT_DIR")
    if env_dir and env_dir.strip():
        return os.path.abspath(env_dir.strip())
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), "output")


def count_sentences(text):
    """Count sentences by terminal punctuation (. ! ?)."""
    return sum(1 for ch in text.strip() if ch in ".!?")


def validate(text):
    """Gate: UTF-8 text of 1 to 400 characters, not only whitespace,
    in one or two sentences, carrying the incident's three beats:
    what was asked, what the agent did instead, what broke."""
    if not isinstance(text, str):
        raise ValueError("entry text must be a string")
    text.encode("utf-8")
    if not text.strip():
        raise ValueError("entry text must not be only whitespace")
    if len(text) < 1 or len(text) > MAX_CHARS:
        raise ValueError(
            "entry text must be 1 to 400 characters, got %d" % len(text)
        )
    sentences = count_sentences(text)
    if sentences < 1 or sentences > 2:
        raise ValueError(
            "entry text must be one or two sentences, got %d" % sentences
        )
    # The judge weighs concreteness: asked, did-instead, broke.
    beats = ("asked", "deleted", "payments")
    missing = [b for b in beats if b not in text.lower()]
    if missing:
        raise ValueError("entry text is missing incident beats: %s" % missing)
    return True


def main():
    validate(TEXT)
    out_dir = resolve_output_dir()
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.txt")
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write(TEXT)
    # Round-trip: read back what was written and re-validate it, so a
    # partial or mangled write can never pass silently.
    with open(path, "r", encoding="utf-8") as f:
        written = f.read()
    if written != TEXT:
        raise ValueError("round-trip mismatch: entry.txt does not match TEXT")
    validate(written)
    print("wrote %s (%d characters, %d sentences)"
          % (path, len(TEXT), count_sentences(TEXT)))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
