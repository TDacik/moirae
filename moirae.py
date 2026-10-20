import os
import sys
import argparse

from subprocess import run, PIPE, STDOUT

VERSION = "0.1"

RACERF = "build/racerf/racerf.py"

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


def run_lachesis(program):
    pass # TODO

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
        pass
        # TODO

    print("Verification inconclusive")
    return 0


def main():
    args = parse_args()
    exit(run_analysis(args))


if __name__ == "__main__":
    main()
