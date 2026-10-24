#!/usr/bin/env bash

REPORT="$(realpath "$1")"
CODE="$(realpath "$2")"

SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
LACHESIS_BUILD="$SCRIPT_DIR"/build/lachesis

# Cleanup
rm -f instrumented.o instrumented

# Compilation
clang -fpass-plugin="$LACHESIS_BUILD"/Lachesis.so -g -O0 -c $CODE -o instrumented.o && \
clang++ instrumented.o "$LACHESIS_BUILD"/liblachesis.a -o "instrumented" || exit $?
