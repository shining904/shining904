#!/usr/bin/env bash
# Audio for the v4 gold short: bright Lyria score (hit at 24.1 s), synthesized sound design,
# and — when MAYOR is set — the mayor's interview audio from 13.5 s (the iris opening), with
# the score ducked under it.
#   tools/mix_gold4.sh                      # no interview audio yet
#   MAYOR=path/to/interview.mp4 tools/mix_gold4.sh
set -euo pipefail
cd "$(dirname "$0")/../shared/assets"
duck() {  # 0..1 dip between $1 and $2 (seconds)
  echo "(clip((t-$1)/0.4,0,1)-clip((t-$2)/0.5,0,1))"
}
if [ -n "${MAYOR:-}" ]; then
  ffmpeg -v error -y -i music-gold3.mp3 -i sfx-gold2.wav -i "$MAYOR" -filter_complex "
[0]volume='1-0.5*$(duck 13.3 18.2)':eval=frame[m];
[1]volume=0.9[s];
[2:a]atrim=0:4.9,afade=t=out:st=4.5:d=0.4,loudnorm=I=-16:TP=-2,adelay=13500|13500,volume=1.6[mv];
[m][s][mv]amix=inputs=3:normalize=0,loudnorm=I=-14:TP=-1.5" -t 37.5 -ar 44100 -b:a 192k music-gold4-mix.mp3
else
  ffmpeg -v error -y -i music-gold3.mp3 -i sfx-gold2.wav -filter_complex "
[1]volume=0.9[s];
[0][s]amix=inputs=2:normalize=0,loudnorm=I=-14:TP=-1.5" -t 37.5 -ar 44100 -b:a 192k music-gold4-mix.mp3
fi
ffmpeg -i music-gold4-mix.mp3 -af ebur128 -f null - 2>&1 | grep "I:" | tail -1
