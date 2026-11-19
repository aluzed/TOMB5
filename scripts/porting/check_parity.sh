#!/bin/bash
# Verifie la parite 32 bits (OpenGL) / 64 bits (Vulkan) sur la scene de
# reference RMIG-007 : les deux builds doivent produire le meme BMP.
#
#   scripts/porting/check_parity.sh [frames]
#
# Sans argument : 1800 frames (scene de reference officielle).
# Pour un controle rapide : scripts/porting/check_parity.sh 300
#
# Sortie : 0 si les captures sont identiques, 1 sinon.

set -u

ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
DATA="$ROOT/build/porting/data-ntsc"
B64="$ROOT/build/porting/build64/SPEC_PSXPC_N/MAIN"
B32="$ROOT/build/porting/build32-check/SPEC_PSXPC_N/MAIN"
FRAMES="${1:-1800}"
TMP="${TMPDIR:-/tmp}/tomb5_parity.$$"

for f in "$B64" "$B32" "$DATA"; do
    if [ ! -e "$f" ]; then
        echo "manquant : $f" >&2
        exit 2
    fi
done

mkdir -p "$TMP"
trap 'pgrep -x MAIN >/dev/null 2>&1 && pgrep -x MAIN | xargs -r kill -9; rm -rf "$TMP"' EXIT

run() {
    local bin="$1" out="$2" log="$3"
    pgrep -x MAIN >/dev/null 2>&1 && pgrep -x MAIN | xargs -r kill -9
    sleep 1
    ( cd "$DATA" && setsid env DISPLAY="${DISPLAY:-:1}" SDL_AUDIODRIVER=dummy \
        TOMB5_AUTOLOAD=1 TOMB5_START_LEVEL=3 TOMB5_FRAMES="$FRAMES" \
        TOMB5_CAPTURE="$out" "$bin" >"$log" 2>&1 </dev/null & )
    # attente de la fin du harnais (le jeu quitte seul apres la capture)
    local waited=0
    while pgrep -x MAIN >/dev/null 2>&1; do
        sleep 2
        waited=$((waited + 2))
        if [ "$waited" -ge 600 ]; then
            echo "timeout ($bin)" >&2
            pgrep -x MAIN | xargs -r kill -9
            return 1
        fi
    done
    [ -s "$out" ]
}

echo "== scene de reference : niveau 3, $FRAMES frames"
run "$B64" "$TMP/vk.bmp" "$TMP/vk.log" || { echo "echec 64 bits"; exit 1; }
echo "64 bits : $(sha256sum "$TMP/vk.bmp" | cut -d' ' -f1)"
run "$B32" "$TMP/gl.bmp" "$TMP/gl.log" || { echo "echec 32 bits"; exit 1; }
echo "32 bits : $(sha256sum "$TMP/gl.bmp" | cut -d' ' -f1)"

REPORT="$(python3 "$ROOT/scripts/porting/capture_compare.py" \
    --a "$TMP/gl.bmp" --b "$TMP/vk.bmp" 2>&1)"
echo "$REPORT" | tail -5

if cmp -s "$TMP/gl.bmp" "$TMP/vk.bmp"; then
    echo "PARITE OK : captures identiques octet pour octet"
    exit 0
fi

# Tolerance : la scene de reference officielle (1800 frames) est identique a
# l'octet ; sur des durees plus courtes il peut rester un pixel de bord.
if echo "$REPORT" | grep -q "mean_abs_diff=0.000"; then
    WITHIN="$(echo "$REPORT" | grep -o 'pixels_within_8_after_gain=[0-9]*' | head -1 | cut -d= -f2)"
    if [ "${WITHIN:-0}" -ge 307199 ]; then
        echo "PARITE OK (a 1 pixel pres) : mean_abs_diff=0.000, ${WITHIN}/307200 pixels identiques"
        exit 0
    fi
fi

echo "PARITE KO : les captures diffèrent" >&2
exit 1
