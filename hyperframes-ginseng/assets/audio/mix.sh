#!/bin/bash
# Builds mix.mp3: the original music track trimmed to the reel length,
# with a short fade-out, normalised for Instagram.
set -euo pipefail
cd "$(dirname "$0")"
LEN=29.33
ffmpeg -v error -y -i music.wav -af "atrim=0:$LEN,afade=t=out:st=$(python3 -c "print($LEN-1.5)"):d=1.5,loudnorm=I=-14:TP=-1.5:LRA=11" -ar 48000 -b:a 192k mix.mp3
