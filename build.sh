#!/usr/bin/env bash

set -euo pipefail

BUILD_DIR="build"
RACERF_REPOSITORY="$BUILD_DIR"/racerf-repository
BUILD_DIR_RACERF="$BUILD_DIR"/racerf
LACHESIS_REPOSITORY="$BUILD_DIR"/lachesis-repository
BUILD_DIR_LACHESIS="$BUILD_DIR"/lachesis

init() {
    # Create build directory
    if [[ -d "$BUILD_DIR" ]]; then
	echo "Removing existing '$BUILD_DIR' directory"
	rm -rf -- "$BUILD_DIR"
    fi

    mkdir -p -- "$BUILD_DIR"
    mkdir -p -- "$BUILD_DIR_RACERF"
    mkdir -p -- "$BUILD_DIR_LACHESIS"
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

build_lachesis() {
    git clone -b svcomp -- https://gitea.jlhko.sk/yokto/lachesis.git $LACHESIS_REPOSITORY
    chmod +x "$LACHESIS_REPOSITORY"/scripts/svcomp/build.sh
    chmod +x "$LACHESIS_REPOSITORY"/scripts/svcomp/docker_build.sh
    (
        cd "$LACHESIS_REPOSITORY" && ./scripts/svcomp/build.sh
    )
    mv "$LACHESIS_REPOSITORY"/build/* "$BUILD_DIR_LACHESIS"
    mv "$LACHESIS_REPOSITORY"/scripts/lachesis_plugin.sh "$BUILD_DIR_LACHESIS"
    mv "$LACHESIS_REPOSITORY"/config.yaml "$BUILD_DIR_LACHESIS"
}

init
build_racerf
build_lachesis
