#!/usr/bin/env python3
"""Load ArchiMate Lite (and kc-base dependency) into a running knowledge-core."""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from _lib.load_catalog import main  # noqa: E402

if __name__ == "__main__":
    raise SystemExit(main(Path(__file__).resolve().parent))
