#!/bin/bash
# Builds mix.mp3 (30 s): melodrama piano bed under the three "개우 도전" days,
# record scratch at 21.75 s, then the bright festival jingle for the ending.
# Rubber-stamp thuds land with each acting-rating stamp. Narration (Jiwoo) ducks the music with smoothstep ramps.
set -euo pipefail
cd "$(dirname "$0")"
LEN=30
NARR=("v1.mp3 0.4 5.75" "v2.mp3 7.5 5.1" "v3.mp3 14.8 3.0" "v4.mp3 22.4 5.56")
DUCK=0.45 RAMP=0.3
ms() { python3 -c "print(int($1*1000))"; }
inputs=(-i drama.wav -i happy.wav -i scratch.mp3 -i sting.mp3)
STAMPS=(5.57 13.17 20.37 22.32)
f="[0:a]aformat=sample_rates=48000:channel_layouts=stereo,atrim=0:22,afade=t=in:d=0.3,afade=t=out:st=21.55:d=0.3,volume=0.8[dr];"
f+="[1:a]aformat=sample_rates=48000:channel_layouts=stereo,atrim=0:8,afade=t=out:st=7.0:d=1.0,volume=0.75,adelay=22000|22000[hp];"
f+="[dr][hp]amix=inputs=2:normalize=0[mus];"
idx=4; labels=""
for n in "${NARR[@]}"; do
  read -r file start len <<<"$n"; inputs+=(-i "$file"); d=$(ms "$start")
  f+="[$idx:a]aformat=sample_rates=48000:channel_layouts=stereo,atrim=0:$len,afade=t=out:st=$(python3 -c "print($len-0.08)"):d=0.08,volume=1.4,adelay=$d|$d[v$idx];"
  labels+="[v$idx]"; idx=$((idx + 1))
done
f+="${labels}amix=inputs=${#NARR[@]}:normalize=0[narr];"
w=""
for n in "${NARR[@]}"; do
  read -r _ start len <<<"$n"
  a=$(python3 -c "print(round($start-0.1-$RAMP,3))"); b=$(python3 -c "print(round($start+$len+0.15+$RAMP,3))")
  w+="+(st(0\\,clip((t-$a)/$RAMP\\,0\\,1))*0+ld(0)*ld(0)*(3-2*ld(0)))*(st(1\\,clip(($b-t)/$RAMP\\,0\\,1))*0+ld(1)*ld(1)*(3-2*ld(1)))"
done
f+="[mus]volume=eval=frame:volume='1-(1-$DUCK)*clip(0${w}\\,0\\,1)'[bed];"
f+="[2:a]aformat=sample_rates=48000:channel_layouts=stereo,volume=0.7,adelay=21750|21750[sc];"
f+="[3:a]aformat=sample_rates=48000:channel_layouts=stereo,volume=0.45,adelay=12230|12230[st];"
sf=""
for t in "${STAMPS[@]}"; do
  inputs+=(-i stamp.mp3); d=$(ms "$t")
  f+="[$idx:a]aformat=sample_rates=48000:channel_layouts=stereo,volume=0.9,adelay=$d|$d[k$idx];"
  sf+="[k$idx]"; idx=$((idx + 1))
done
f+="[bed][narr][sc][st]${sf}amix=inputs=$((4 + ${#STAMPS[@]})):normalize=0,loudnorm=I=-14:TP=-1.5:LRA=11,apad,atrim=0:$LEN[out]"
ffmpeg -v error -y "${inputs[@]}" -filter_complex "$f" -map "[out]" -ar 48000 -b:a 192k mix.mp3
