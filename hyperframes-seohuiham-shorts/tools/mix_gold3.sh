#!/usr/bin/env bash
# Final audio for the extended gold short: bright Lyria score (hit shifted to 24.1 s),
# synthesized sound design, and Seo Hui's closing line at 32.8 s with the score ducked under it.
set -euo pipefail
cd "$(dirname "$0")/../shared/assets"
VO=32.8
ffmpeg -v error -y -i music-gold3.mp3 -i sfx-gold2.wav -i voice-safe.mp3 -filter_complex "
[0]volume='1-0.5*(clip((t-32.5)/0.4,0,1)-clip((t-35.8)/0.5,0,1))':eval=frame[m];
[1]volume=0.9[s];
[2]loudnorm=I=-16:TP=-2,adelay=$(python3 -c "print(int($VO*1000))")|$(python3 -c "print(int($VO*1000))"),volume=1.6[v];
[m][s][v]amix=inputs=3:normalize=0,loudnorm=I=-14:TP=-1.5" -t 37.5 -ar 44100 -b:a 192k music-gold3-mix.mp3
ffmpeg -i music-gold3-mix.mp3 -af ebur128 -f null - 2>&1 | grep "I:" | tail -1
