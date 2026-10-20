#!/usr/bin/env bash

set -euo pipefail

BUILD_DIR="build"
RACERF_REPOSITORY="$BUILD_DIR"/racerf-repository
BUILD_DIR_RACERF="$BUILD_DIR"/racerf

init() {
    # Create build directory
    if [[ -d "$BUILD_DIR" ]]; then
	echo "Removing existing '$BUILD_DIR' directory"
	rm -rf -- "$BUILD_DIR"
    fi

    mkdir -p -- "$BUILD_DIR"
    mkdir -p -- "$BUILD_DIR_RACERF"
}

# Download and setup RacerF as a standalone script
build_racerf() {
    git clone -- https://github.com/TDacik/RacerF $RACERF_REPOSITORY

    (
        cd "$RACERF_REPOSITORY"/scripts/sv-comp && ./build_standalone_bin.sh
    )

    mv "$RACERF_REPOSITORY"/scripts/*.py "$BUILD_DIR_RACERF"
    mv "$RACERF_REPOSITORY"/models "$BUILD_DIR_RACERF"
    mv "$RACERF_REPOSITORY"/scripts/sv-comp/_opam "$BUILD_DIR_RACERF"
}

init
build_racerf
