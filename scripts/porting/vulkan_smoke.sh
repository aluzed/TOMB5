#!/bin/bash
# Build and run the RMIG-009 Vulkan smoke test.
set -e
ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
OUT="${TMPDIR:-/tmp}/tomb5_vulkan_smoke"
g++ -std=c++17 -O2 "$ROOT/tools/vulkan_smoke.cpp" -o "$OUT" \
    $(sdl2-config --cflags --libs) -lvulkan
DISPLAY="${DISPLAY:-:1}" timeout 40 "$OUT"
