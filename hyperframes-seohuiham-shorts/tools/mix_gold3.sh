#!/usr/bin/env bash
# Final audio for the extended gold short: bright Lyria score (hit shifted to 24.1 s),
# synthesized sound design, and Seo Hui's two lines — the congratulation at 13.7 s and the
# safe-voyage line at 32.8 s — with the score ducked under each.
set -euo pipefail
cd "$(dirname "$0")/../shared/assets"
duck() {  # 0..1 dip between $1 and $2 (seconds)
  echo "(clip((t-$1)/0.4,0,1)-clip((t-$2)/0.5,0,1))"
}
ffmpeg -v error -y -i music-gold3.mp3 -i sfx-gold2.wav -i voice-congrats.mp3 -i voice-safe.mp3 -filter_complex "
[0]volume='1-0.5*($(duck 13.4 17.8)+$(duck 32.5 35.8))':eval=frame[m];
[1]volume=0.9[s];
[2]atempo=1.08,loudnorm=I=-16:TP=-2,adelay=13700|13700,volume=1.6[v1];
[3]loudnorm=I=-16:TP=-2,adelay=32800|32800,volume=1.6[v2];
[m][s][v1][v2]amix=inputs=4:normalize=0,loudnorm=I=-14:TP=-1.5" -t 37.5 -ar 44100 -b:a 192k music-gold3-mix.mp3
ffmpeg -i music-gold3-mix.mp3 -af ebur128 -f null - 2>&1 | grep "I:" | tail -1
