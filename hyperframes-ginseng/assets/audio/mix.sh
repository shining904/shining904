#!/bin/bash
# Builds mix.mp3 for the ginseng reel: the original music track with the
# leader ginseng's deadpan lines (v1-v7) on the caption bars. The music
# dips to DUCK of its level under each line (0.25 s ramps), then the
# whole mix is normalised for Instagram.
set -euo pipefail
cd "$(dirname "$0")"
LEN=29.33
DUCK=0.7
RAMP=0.25
# voice: file start(s) speech-length(s) — starts sit just after each caption bar
VOICE=("v1.mp3 0.25 3.45" "v2.mp3 4.07 2.4" "v3.mp3 7.97 1.9" "v4.mp3 11.87 2.3"
       "v5.mp3 15.78 2.25" "v6.mp3 19.68 1.95" "v7.mp3 23.75 5.3")

inputs=(-i music.wav)
labels=""
windows=""
idx=1
for v in "${VOICE[@]}"; do
  read -r file start len <<<"$v"
  inputs+=(-i "$file")
  ms=$(python3 -c "print(int($start*1000))")
  labels+="[$idx:a]aformat=sample_rates=48000:channel_layouts=stereo,atrim=0:$len,afade=t=out:st=$(python3 -c "print($len-0.08)"):d=0.08,volume=1.6,adelay=$ms|$ms[v$idx];"
  a=$(python3 -c "print(round($start-0.15-$RAMP,3))"); b=$(python3 -c "print(round($start+$len+0.15+$RAMP,3))")
  windows+="+clip((t-$a)/$RAMP\\,0\\,1)*clip(($b-t)/$RAMP\\,0\\,1)"
  idx=$((idx + 1))
done
vl=""; for i in $(seq 1 ${#VOICE[@]}); do vl+="[v$i]"; done
filters="[0:a]aformat=sample_rates=48000:channel_layouts=stereo,atrim=0:$LEN,afade=t=out:st=$(python3 -c "print($LEN-1.5)"):d=1.5,volume=eval=frame:volume='1-(1-$DUCK)*clip(0${windows}\\,0\\,1)'[bed];"
filters+="${labels}${vl}amix=inputs=${#VOICE[@]}:normalize=0[voice];"
filters+="[bed][voice]amix=inputs=2:normalize=0,loudnorm=I=-14:TP=-1.5:LRA=11,atrim=0:$LEN[out]"
ffmpeg -v error -y "${inputs[@]}" -filter_complex "$filters" -map "[out]" -ar 48000 -b:a 192k mix.mp3
