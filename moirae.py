#!/usr/bin/env python3

import os
import sys
import argparse

from pathlib import Path
from subprocess import run, PIPE, STDOUT

VERSION = "0.1"

SCRIPT_DIR = Path(__file__).resolve().parent
RACERF = SCRIPT_DIR / "build/racerf/racerf.py"
LACHESIS = SCRIPT_DIR / "build/lachesis/lachesis_plugin.sh"

REPORT_FILE = "report.yml"


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
        exit(res.returncode)

    is_race_free = "[racer] Data race " not in str(res.stdout)
    return is_race_free


def run_lachesis(args):
    cmd = [
        LACHESIS,
        REPORT_FILE,
        args.source_program,
    ]
    res = run(cmd, stdout=PIPE, stderr=STDOUT, universal_newlines=True)
    if res.returncode != 0:
        print(res.stdout)
        exit(res.returncode)

    is_race_free = "[lachesis] Data race " not in str(res.stdout)
    return is_race_free

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--version", action="version", version=VERSION)
    parser.add_argument("--data-model", type=str, default="ILP32")
    parser.add_argument("source_program")
    return parser.parse_args()


def run_analysis(args):
    if run_racerf(args):
        print("Program proved racer-free by RacerF")
        return 0
    elif run_lachesis(args):
        print("No race was observed by Lachesis")
        return 0

    print("Verification inconclusive")
    return 0


def main():
    args = parse_args()
    exit(run_analysis(args))


if __name__ == "__main__":
    main()
