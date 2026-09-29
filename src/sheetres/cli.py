"""`sheetres <sample-folder>`: print mean and SD of Rs, rho and sigma for one sample."""

from __future__ import annotations

import argparse
import sys
from collections.abc import Sequence
from pathlib import Path

from sheetres.parser import InputFormatError, load_sample
from sheetres.stats import SampleSummary, summarize

EXIT_INPUT_ERROR = 2


def format_summary(s: SampleSummary) -> str:
    rows = [
        ("Mean sheet resistance", s.rs_mean_ohm_sq, "Ohm/square"),
        ("Std. dev. of mean sheet resistance", s.rs_sd_ohm_sq, "Ohm/square"),
        ("Mean resistivity", s.rho_mean_ohm_m, "Ohm.m"),
        ("Std. dev. of mean resistivity", s.rho_sd_ohm_m, "Ohm.m"),
        ("Mean conductivity", s.sigma_mean_s_per_m, "S/m"),
        ("Std. dev. of mean conductivity", s.sigma_sd_s_per_m, "S/m"),
    ]
    width = max(len(label) for label, _, _ in rows)
    lines = [f"Sample {s.sample}  (n = {s.n} measurements, population SD)"]
    lines += [f"  {label:<{width}}  {value:.6g} {unit}" for label, value, unit in rows]
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
