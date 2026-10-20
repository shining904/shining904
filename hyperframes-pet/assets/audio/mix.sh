#!/bin/bash
# Builds mix.mp3 (30 s): mock-tragic opera bed under the three "개우 도전" days with the
# day-by-day narration, record scratch at 21.75 s, then a bouncy jersey-club beat
# under the festival call-out.
# Rubber-stamp thuds land with each acting-rating stamp. Narration ducks the music with smoothstep ramps.
set -euo pipefail
cd "$(dirname "$0")"
LEN=30
# VO=b: bright, bubbly Ha-Rin (eleven v3); VO=c: the same takes pitched up ~3.4 semitones
# with shifted formants for a cartoon-character voice. OUT names the result.
VO=${VO:-b}; OUT=${OUT:-mix.mp3}
NARR=("${VO}1.mp3 0.3 4.6" "${VO}2.mp3 7.6 4.1" "${VO}3.mp3 14.8 2.85" "${VO}4.mp3 22.4 6.19")
DUCK=0.4 RAMP=0.3
ms() { python3 -c "print(int($1*1000))"; }
inputs=(-i opera.wav -i club.wav -i scratch.mp3 -i sting.mp3)
STAMPS=(5.57 13.17 20.37 22.32)
f="[0:a]aformat=sample_rates=48000:channel_layouts=stereo,atrim=0:22,afade=t=in:d=0.2,afade=t=out:st=21.55:d=0.3,volume=1.4[dr];"
f+="[1:a]aformat=sample_rates=48000:channel_layouts=stereo,atrim=14:22,asetpts=PTS-STARTPTS,afade=t=out:st=7.2:d=0.8,volume=2.2,adelay=22000|22000[hp];"
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
ffmpeg -v error -y "${inputs[@]}" -filter_complex "$f" -map "[out]" -ar 48000 -b:a 192k "$OUT"
