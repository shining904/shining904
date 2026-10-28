#!/bin/bash
# Encode a transparent PNG sequence (f_0001.png …) to a VP9 WebM with alpha that Chrome,
# and so HyperFrames, plays over any background:  encode_alpha.sh frames/ out.webm [fps]
set -euo pipefail
ffmpeg -v error -y -framerate "${3:-30}" -i "$1/f_%04d.png" -c:v libvpx-vp9 -pix_fmt yuva420p \
  -b:v 0 -crf 26 -row-mt 1 -auto-alt-ref 0 "$2"
echo "$2"
