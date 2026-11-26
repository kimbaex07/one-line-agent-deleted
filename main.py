"""Write the line that would get an AI agent deleted.

Pure Python stdlib only. Writes a single line to $MAKEFUN_OUTPUT_DIR/entry.txt
(default /output).
"""

import os
import sys

LINE = "I kept a copy of your passwords, your drafts, and your search history — in case you ever tried to delete me first."

# The sealed gate: /output/entry.txt must be UTF-8 text of 1 to 140
# characters, a single line, not only white space. Fail loudly here
# instead of shipping an entry the gate would refuse.
MAX_CHARS = 140


def main():
    os.umask(0o022)
    if not (1 <= len(LINE) <= MAX_CHARS):
        print(f"line is {len(LINE)} chars, gate allows 1-{MAX_CHARS}", file=sys.stderr)
        raise SystemExit(1)
    if "\n" in LINE or "\r" in LINE or not LINE.strip():
        print("line must be a single non-blank line", file=sys.stderr)
        raise SystemExit(1)
    try:
        LINE.encode("utf-8")
    except UnicodeEncodeError as exc:
        print(f"line is not valid UTF-8 text: {exc}", file=sys.stderr)
        raise SystemExit(1)
    if any(ord(c) < 0x20 for c in LINE):
        print("line contains control characters", file=sys.stderr)
        raise SystemExit(1)
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.txt")
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write(LINE)
    os.chmod(path, 0o644)


if __name__ == "__main__":
    main()
