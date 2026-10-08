#!/bin/bash
# Builds mix.mp3 for the AI vibe-coding promo: the 127 BPM tech-pop bed (music.mp3) under
# one continuous narration take (narr.mp3, Jiwoo). The music eases down to DUCK under
# each spoken phrase (smoothstep ramps: ATTACK before, RELEASE after), then the whole
# mix is normalised for Instagram.
set -euo pipefail
cd "$(dirname "$0")"
LEN=30.0
NARR_START=0.5
# music.mp3 is mastered at about -13 LUFS; 0.24 keeps it under the voice.
GAIN=0.24
DUCK=0.5
ATTACK=0.3
RELEASE=0.5
# Spoken phrases inside narr.mp3 (start end, file time), from silencedetect.
PHRASES=("0 1.70" "2.15 5.86" "6.38 11.13" "11.65 18.59" "18.89 25.46" "25.85 28.16")

windows=""
for p in "${PHRASES[@]}"; do
  read -r s e <<<"$p"
  a=$(python3 -c "print(round($NARR_START+$s-0.1-$ATTACK,3))"); b=$(python3 -c "print(round($NARR_START+$e+0.1+$RELEASE,3))")
  windows+="+clip((t-$a)/$ATTACK\\,0\\,1)*clip(($b-t)/$RELEASE\\,0\\,1)"
done
ms=$(python3 -c "print(int($NARR_START*1000))")
# s = how far into a duck we are (0..1); smoothstep s*s*(3-2*s) makes the dips ease in and out.
s="clip(0${windows}\\,0\\,1)"
filters="[0:a]aformat=sample_rates=48000:channel_layouts=stereo,atrim=0:$LEN,volume=$GAIN,afade=t=out:st=$(python3 -c "print($LEN-1.5)"):d=1.5,volume=eval=frame:volume='1-(1-$DUCK)*$s*$s*(3-2*$s)'[bed];"
filters+="[1:a]aformat=sample_rates=48000:channel_layouts=stereo,volume=1.4,adelay=$ms|$ms[voice];"
filters+="[bed][voice]amix=inputs=2:normalize=0,loudnorm=I=-14:TP=-1.5:LRA=11,atrim=0:$LEN[out]"
ffmpeg -v error -y -i music.mp3 -i narr.mp3 -filter_complex "$filters" -map "[out]" -ar 48000 -b:a 192k mix.mp3
