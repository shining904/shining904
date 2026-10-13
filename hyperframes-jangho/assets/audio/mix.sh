#!/bin/bash
# Builds mix.mp3 (60 s) for the 장호원 bid draft: narration n1-n8 on their cues,
# the Lyria score (delayed 1 s so its climax lands on the benefits/slogan) ducked
# under the voice with a smooth envelope, clip natural sound and soft impacts.
set -euo pipefail
cd "$(dirname "$0")"
LEN=60
NARR=("n1.mp3 1.0 3.5" "n2.mp3 7.2 4.85" "n3.mp3 13.8 6.75" "n4.mp3 23.8 3.6"
      "n5.mp3 28.0 7.4" "n6.mp3 36.2 4.6" "n7.mp3 42.8 3.7" "n8.mp3 54.2 3.2")
CLIPS=("../clips/dawn-graded.mp4 0 6.8 0.45" "../clips/race.mp4 6.6 6.8 0.4"
       "../clips/farm.mp4 13.2 10.3 0.2" "../clips/aerial.mp4 48.2 5.6 0.25")
IMPACT=(2.3 9.5 25.1 55.2)
GAIN=0.55 DUCK=0.5 RAMP=0.35
ms() { python3 -c "print(int($1*1000))"; }
inputs=(-i music.mp3)
filters="[0:a]aformat=sample_rates=48000:channel_layouts=stereo,afade=t=out:st=56.4:d=1.5,adelay=1000|1000,volume=$GAIN[mus];"
idx=1; labels=""
for n in "${NARR[@]}"; do
  read -r file start len <<<"$n"; inputs+=(-i "$file"); d=$(ms "$start")
  filters+="[$idx:a]aformat=sample_rates=48000:channel_layouts=stereo,atrim=0:$len,afade=t=out:st=$(python3 -c "print($len-0.08)"):d=0.08,adelay=$d|$d[v$idx];"
  labels+="[v$idx]"; idx=$((idx + 1))
done
filters+="${labels}amix=inputs=${#NARR[@]}:normalize=0[narr];"
windows=""
for n in "${NARR[@]}"; do
  read -r _ start len <<<"$n"
  a=$(python3 -c "print(round($start-0.15-$RAMP,3))"); b=$(python3 -c "print(round($start+$len+0.2+$RAMP,3))")
  # smoothstep ramps on each side
  windows+="+(st(0\\,clip((t-$a)/$RAMP\\,0\\,1))*0+ld(0)*ld(0)*(3-2*ld(0)))*(st(1\\,clip(($b-t)/$RAMP\\,0\\,1))*0+ld(1)*ld(1)*(3-2*ld(1)))"
done
filters+="[mus]volume=eval=frame:volume='1-(1-$DUCK)*clip(0${windows}\\,0\\,1)'[bed];"
fx=""
for c in "${CLIPS[@]}"; do
  read -r file start len vol <<<"$c"; inputs+=(-i "$file"); d=$(ms "$start")
  filters+="[$idx:a]aformat=sample_rates=48000:channel_layouts=stereo,atrim=0:$len,afade=t=in:d=0.2,afade=t=out:st=$(python3 -c "print($len-0.4)"):d=0.4,volume=$vol,adelay=$d|$d[f$idx];"
  fx+="[f$idx]"; idx=$((idx + 1))
done
for t in "${IMPACT[@]}"; do
  inputs+=(-i impact.mp3); d=$(ms "$t")
  filters+="[$idx:a]aformat=sample_rates=48000:channel_layouts=stereo,volume=0.06,adelay=$d|$d[f$idx];"
  fx+="[f$idx]"; idx=$((idx + 1))
done
count=$((2 + ${#CLIPS[@]} + ${#IMPACT[@]}))
filters+="[bed][narr]${fx}amix=inputs=$count:normalize=0,loudnorm=I=-14:TP=-1.5:LRA=11,apad,atrim=0:$LEN[out]"
ffmpeg -v error -y "${inputs[@]}" -filter_complex "$filters" -map "[out]" -ar 48000 -b:a 192k mix.mp3
