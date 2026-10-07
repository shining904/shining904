#!/bin/bash
# Builds mix.mp3 for the ginseng reel: the 128 BPM dance track (music3.mp3) with the
# narrator and leader ginseng lines on the caption bars. The music
# dips to DUCK of its level under each line (0.25 s ramps), then the
# whole mix is normalised for Instagram.
set -euo pipefail
cd "$(dirname "$0")"
LEN=30.0
# music3.mp3 is mastered ~9dB hotter than the old bed, hence volume=0.34 on it.
DUCK=0.7
RAMP=0.25
# voice: file start(s) speech-length(s). n1/n7 are the off-screen narrator (Ha-Rin);
# v2-v6 are the leader ginseng. v2 and v5/v6 are lip-synced inside the leader and
# close-up clips (clip starts 0 and 15.0), so their times are fixed.
# n1-tight.wav is n1.mp3 with its middle pause shortened and 10% faster.
VOICE=("n1-tight.wav 0.15 3.62" "v2.mp3 4.07 2.4" "v3.mp3 7.62 1.9" "v4.mp3 11.35 2.3"
       "v5.mp3 15.105 2.25" "v6.mp3 19.005 1.95" "n7.mp3 22.64 6.25")

inputs=(-i music3.mp3)
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
filters="[0:a]aformat=sample_rates=48000:channel_layouts=stereo,atrim=0:$LEN,volume=0.34,afade=t=out:st=$(python3 -c "print($LEN-1.5)"):d=1.5,volume=eval=frame:volume='1-(1-$DUCK)*clip(0${windows}\\,0\\,1)'[bed];"
filters+="${labels}${vl}amix=inputs=${#VOICE[@]}:normalize=0[voice];"
filters+="[bed][voice]amix=inputs=2:normalize=0,loudnorm=I=-14:TP=-1.5:LRA=11,atrim=0:$LEN[out]"
ffmpeg -v error -y "${inputs[@]}" -filter_complex "$filters" -map "[out]" -ar 48000 -b:a 192k mix.mp3
