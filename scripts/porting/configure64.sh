#!/bin/sh
# Configure et construit la cible **64 bits** (RMIG-002).
#
# Le backend OpenGL y est encore utilisé, uniquement comme filet de sécurité
# pendant la migration : GLEW 64 bits n'étant pas installé sur la machine, ce
# script le compile depuis les sources vendored. Il disparaîtra avec
# RMIG-012 (retrait d'OpenGL au profit de Vulkan).
#
# Usage :
#   scripts/porting/configure64.sh [build-dir] [--build]
#
# Par défaut : build/porting/build64. Le script refuse d'écraser un arbre
# existant (supprimez-le explicitement).
set -eu

ROOT=$(cd "$(dirname "$0")/../.." && pwd)
BUILD=${1:-$ROOT/build/porting/build64}
DO_BUILD=0
[ "${2:-}" = "--build" ] && DO_BUILD=1

GLEW_SRC=${GLEW_SRC:-/tmp/opencode/glew/glew-2.2.0}
GLEW_OUT=${GLEW_OUT:-/tmp/opencode/glew64}

if [ -d "$BUILD" ]; then
	echo "configure64: $BUILD existe déjà ; supprimez-le pour reconfigurer" >&2
	exit 1
fi

# --- GLEW 64 bits (bootstrap, temporaire) -------------------------------
if [ ! -f "$GLEW_OUT/libGLEW.a" ]; then
	echo "configure64: construction de GLEW 64 bits dans $GLEW_OUT"
	mkdir -p "$GLEW_OUT"
	gcc -O2 -fPIC -DGLEW_NO_GLU -I"$GLEW_SRC/include" \
		-c "$GLEW_SRC/src/glew.c" -o "$GLEW_OUT/glew.o"
	ar rcs "$GLEW_OUT/libGLEW.a" "$GLEW_OUT/glew.o"
fi

# --- configuration ------------------------------------------------------
# -DGLEW_NO_GLU : GL/glu.h (libglu1-mesa-dev) n'est pas installé en 64 bits.
cmake -S "$ROOT" -B "$BUILD" \
	-DCMAKE_BUILD_TYPE=Debug \
	-DBETA_VERSION=OFF -DDEBUG_VERSION=OFF \
	-DDISC_VERSION=ON -DNTSC_VERSION=ON \
	-DPSXPC_TEST=ON -DRELOC=OFF -DUSE_32_BIT_ADDR=ON \
	-DCMAKE_C_FLAGS="-DGLEW_NO_GLU" \
	-DCMAKE_CXX_FLAGS="-DGLEW_NO_GLU" \
	-DGLEW_INCLUDE_DIR="$GLEW_SRC/include" \
	-DGLEW_LIBRARY="$GLEW_OUT/libGLEW.a" \
	-DSDL2_INCLUDE_DIR=/usr/include/SDL2 \
	-DSDL2_LIBRARY=/usr/lib/x86_64-linux-gnu/libSDL2.so

if [ "$DO_BUILD" = 1 ]; then
	cmake --build "$BUILD" -j4
	BIN="$BUILD/SPEC_PSXPC_N/MAIN"
	file "$BIN"
	echo "configure64: binaire $BIN"
fi
