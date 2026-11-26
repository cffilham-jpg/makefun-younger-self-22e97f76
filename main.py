"""Write and verify one message to a younger self.
The guitar's broken promise gives the line its specific, lived turn.
"""

import hashlib
import os
import tempfile
from pathlib import Path

LINE = "You will sell the guitar you swore you'd keep forever."
CHAR_LIMIT = 200


def _resolve_output_dir() -> Path:
    env_dir = os.environ.get("MAKEFUN_OUTPUT_DIR")
    if env_dir:
        path = Path(env_dir)
        path.mkdir(parents=True, exist_ok=True)
        return path
    try:
        out = Path("out")
        out.mkdir(parents=True, exist_ok=True)
        return out
    except OSError:
        return Path(tempfile.mkdtemp(prefix="makefun-younger-self-22e97f76-"))


def validate(path: Path) -> None:
    data = path.read_bytes()
    text = data.decode("utf-8")
    if text != LINE:
        raise ValueError("entry.txt content differs from the chosen LINE")
    if not 1 <= len(text) <= CHAR_LIMIT:
        raise ValueError("entry.txt length must be between 1 and 200 characters")
    if "\n" in text or "\r" in text:
        raise ValueError("entry.txt contains a line break")
    if text.endswith("\n"):
        raise ValueError("entry.txt has a trailing newline")
    if text != text.strip():
        raise ValueError("entry.txt has leading or trailing whitespace")


def main() -> None:
    out_dir = _resolve_output_dir()
    entry = out_dir / "entry.txt"
    entry.write_bytes(LINE.encode("utf-8"))
    validate(entry)
    print(hashlib.sha256(LINE.encode("utf-8")).hexdigest())


if __name__ == "__main__":
    main()
