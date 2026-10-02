#!/usr/bin/env python3
"""Compile every .py file in the repository with a bad escape sequence promoted to an error.

py_compile and compileall treat a bad escape sequence as a warning, not a failure, so a
file with one can ship in a wheel and still pass a normal build. CPython reports it as a
DeprecationWarning before 3.12 and a SyntaxWarning from 3.12 on, so this script promotes
both. It also catches any IndentationError or SyntaxError, across the repository source
tree, not only the installed package. It excludes directories that hold no repository
source (a build output, an installed virtual environment), and it compiles each file in
memory, so it writes no .pyc bytecode into the tree.
"""
import pathlib
import sys
import warnings

ROOT = pathlib.Path(__file__).resolve().parent.parent
EXCLUDED_DIRS = {".git", "build", "dist", ".venv", "venv", "__pycache__"}


def is_excluded(path: pathlib.Path) -> bool:
    parts = path.relative_to(ROOT).parts
    return any(part in EXCLUDED_DIRS or part.endswith(".egg-info") for part in parts)


def main() -> int:
    warnings.simplefilter("error", SyntaxWarning)
    warnings.simplefilter("error", DeprecationWarning)
    failures = []
    py_files = sorted(p for p in ROOT.rglob("*.py") if not is_excluded(p))
    for path in py_files:
        try:
            compile(path.read_bytes(), str(path), "exec")
        except (SyntaxError, SyntaxWarning, DeprecationWarning) as exc:
            failures.append((path, exc))

    for path, exc in failures:
        print(f"FAIL: {path.relative_to(ROOT)}: {exc}")

    print(f"{len(py_files)} files checked, {len(failures)} failed")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
