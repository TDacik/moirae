#!/usr/bin/env python3

import os
import sys
import argparse

from pathlib import Path
from subprocess import run, PIPE, STDOUT

VERSION = "0.1"

SCRIPT_DIR = Path(__file__).resolve().parent
RACERF = SCRIPT_DIR / "build/racerf/racerf.py"
LACHESIS_COMPILE = SCRIPT_DIR / "lachesis_compile.sh"
INSTRUMENTED_BIN = SCRIPT_DIR / "instrumented"

REPORT_FILE = "racerf_result.yml"


def run_racerf(args):
    translation = {"ilp32": "gcc_x86_32", "lp64": "gcc_x86_64"}
    frama_c_machdep = translation.get(args.data_model.lower())

    cmd = [
        RACERF,
        "--sv-comp",
        "--over-approx",
        "-machdep",
        frama_c_machdep,
        "-racer-report",
        REPORT_FILE,
        args.source_program,
    ]

    res = run(cmd, stdout=PIPE, stderr=STDOUT, universal_newlines=True)
    if res.returncode != 0:
        print(res.stdout)
        print("RacerF failed")
        exit(res.returncode)

    is_race_free = "[racer] Data race " not in str(res.stdout)
    return is_race_free


def lachesis_compile(args):
    cmd = [
        LACHESIS_COMPILE,
        REPORT_FILE,
        args.source_program,
    ]
    res = run(cmd, stdout=PIPE, stderr=STDOUT, universal_newlines=True)
    if res.returncode != 0:
        print(res.stdout)
        print("Lachesis failed: compilation")
        exit(res.returncode)

def run_instrumented(args, timeout=None):
    cmd = [INSTRUMENTED_BIN]
    res = run(cmd, timeout=timeout, stdout=PIPE, stderr=STDOUT, universal_newlines=True)
    if res.returncode != 0:
        print(res.stdout)
        print("Lachesis failed: instrumented binary crashed")
        exit(res.returncode)

    has_race = "[lachesis] Data race " in str(res.stdout)
    return has_race


def run_lachesis(args):
    limit = None if args.sv_comp else 5

    lachesis_compile()

    i = 0
    while limit is None or i < limit:
        print("[moirae] Lachesis iteration: %d", i)
        run_lachesis_once(args)
        i += 1


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--version", action="version", version=VERSION)
    parser.add_argument("--sv-comp", action="store_true")
    parser.add_argument("--data-model", type=str, default="ILP32")
    parser.add_argument("source_program")
    return parser.parse_args()


def run_analysis(args):
    if run_racerf(args):
        print("Verification successful: program was proved race-free by RacerF")
        return 0
    elif run_lachesis(args):
        print("Data race found by Lachesis")
        return 0

    print("Verification inconclusive")
    return 0


def main():
    if os.path.exists(REPORT_FILE):
        os.remove(REPORT_FILE)
    args = parse_args()
    exit(run_analysis(args))


if __name__ == "__main__":
    main()
