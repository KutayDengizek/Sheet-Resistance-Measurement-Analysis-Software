"""`sheetres <sample-folder>`: print mean and SD of Rs, rho and sigma for one sample."""

from __future__ import annotations

import argparse
import sys
from collections.abc import Sequence
from pathlib import Path

from sheetres.parser import InputFormatError, load_sample
from sheetres.report import QUANTITIES, display, value
from sheetres.stats import SampleSummary, summarize

EXIT_INPUT_ERROR = 2


def format_summary(s: SampleSummary) -> str:
    width = max(len(q.label) for q in QUANTITIES)
    lines = [f"Sample {s.sample}  (n = {s.n} measurements, sample SD with n-1)"]
    lines += [f"  {q.label:<{width}}  {display(value(s, q))} {q.unit}" for q in QUANTITIES]
    return "\n".join(lines)


def main(argv: Sequence[str] | None = None) -> int:
    ap = argparse.ArgumentParser(prog="sheetres", description=__doc__)
    ap.add_argument("folder", type=Path, help="sample folder, e.g. data/260902_U1")
    args = ap.parse_args(argv)
    try:
        summary = summarize(load_sample(args.folder))
    except InputFormatError as exc:
        print(f"sheetres: error: {exc}", file=sys.stderr)
        return EXIT_INPUT_ERROR
    print(format_summary(summary))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
