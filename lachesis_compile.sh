#!/usr/bin/env bash

REPORT="$(realpath "$1")"
CODE="$(realpath "$2")"

SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
LACHESIS_BUILD="$SCRIPT_DIR"/build/lachesis

# Cleanup
rm -f /tmp/instrumented.o /tmp/instrumented

# Compilation
clang -fpass-plugin="$LACHESIS_BUILD"/Lachesis.so -g -O0 -c $CODE -o /tmp/instrumented.o && \
clang++ /tmp/instrumented.o "$LACHESIS_BUILD"/liblachesis.a -o /tmp/instrumented || exit $?
