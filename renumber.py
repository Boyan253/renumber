#!/usr/bin/env python3
"""Rename a set of files into a numbered pattern, safely."""

import argparse
import os
import re
import sys

__version__ = "0.1.0"

SORTS = {
    "name": lambda p: natural_key(os.path.basename(p)),
    "mtime": lambda p: os.path.getmtime(p),
    "size": lambda p: os.path.getsize(p),
}


def natural_key(text):
    """Sort 'img2' before 'img10'."""
    return [int(part) if part.isdigit() else part.lower()
            for part in re.split(r"(\d+)", text)]


def plan(paths, pattern, start=1, step=1, sort="name", reverse=False):
    """Return [(old, new)] without touching the filesystem."""
    ordered = sorted(paths, key=SORTS[sort], reverse=reverse)
    pairs = []
    number = start
    for path in ordered:
        directory, base = os.path.split(path)
        stem, ext = os.path.splitext(base)
        new_name = pattern.format(n=number, name=stem, ext=ext, i=number - start)
        pairs.append((path, os.path.join(directory, new_name)))
        number += step
    return pairs


def check(pairs):
    """Return a list of problems with a rename plan."""
    problems = []
    targets = {}
    sources = {os.path.abspath(old) for old, _ in pairs}
    for old, new in pairs:
        key = os.path.abspath(new)
        if key in targets:
            problems.append("two files would become %s" % new)
        targets[key] = old
        if os.path.exists(new) and key not in sources:
            problems.append("%s already exists" % new)
    return problems


def apply(pairs):
    """Rename via temporary names so swaps and rotations work."""
    temps = []
    for i, (old, _new) in enumerate(pairs):
        tmp = old + ".renumber-%d.tmp" % i
        os.rename(old, tmp)
        temps.append(tmp)
    for tmp, (_old, new) in zip(temps, pairs):
        os.rename(tmp, new)
    return len(pairs)


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--version", action="version",
                    version="%(prog)s " + __version__)
    ap.add_argument("files", nargs="+", help="files to rename (shell glob)")
    ap.add_argument("-p", "--pattern", default="{n:03d}{ext}",
                    help="target name; fields: {n} {i} {name} {ext}")
    ap.add_argument("--start", type=int, default=1)
    ap.add_argument("--step", type=int, default=1)
    ap.add_argument("--sort", default="name", choices=sorted(SORTS))
    ap.add_argument("--reverse", action="store_true")
    ap.add_argument("--apply", action="store_true",
                    help="actually rename; without this it is a dry run")
    args = ap.parse_args(argv)

    files = [p for p in args.files if os.path.isfile(p)]
    if not files:
        print("renumber: no files matched", file=sys.stderr)
        return 2
    pairs = plan(files, args.pattern, args.start, args.step, args.sort, args.reverse)
    problems = check(pairs)
    for old, new in pairs:
        print("%s -> %s" % (os.path.basename(old), os.path.basename(new)))
    for problem in problems:
        print("problem: %s" % problem, file=sys.stderr)
    if problems:
        return 1
    if args.apply:
        print("renamed %d file(s)" % apply(pairs), file=sys.stderr)
    else:
        print("dry run -- pass --apply to rename", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
