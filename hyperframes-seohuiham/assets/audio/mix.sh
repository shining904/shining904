#!/bin/bash
# Builds mix.mp3: the Lyria score (MUSIC, default epic.mp3 for the 73 s cut; music.mp3 + LEN=78 for v1) under every spoken line (narrator n1-n4, young Seo Hui
# y1, mature Seo Hui s1). Each voice is levelled to -18 LUFS, the score dips to DUCK under the
# voices with smoothstep ramps, and the whole mix is normalised to -14 LUFS.
# Line cues come from ../../work/lines.json, written by build.py.
set -euo pipefail
cd "$(dirname "$0")"
MUSIC=${MUSIC:-epic.mp3} LEN=${LEN:-73} GAIN=0.5 DUCK=0.5 RAMP=0.4
mapfile -t NARR < <(python3 -c "import json;[print(f,s,d) for f,s,d in json.load(open('../../work/lines.json'))]")
ms() { python3 -c "print(int($1*1000))"; }
inputs=(-i "$MUSIC")
f="[0:a]aformat=sample_rates=48000:channel_layouts=stereo,atrim=0:$LEN,afade=t=in:d=1.0,afade=t=out:st=$(python3 -c "print($LEN-2.5)"):d=2.5,volume=$GAIN[mus];"
idx=1; labels=""; w=""
for n in "${NARR[@]}"; do
  read -r file start len <<<"$n"; inputs+=(-i "$file"); d=$(ms "$start")
  f+="[$idx:a]aformat=sample_rates=48000:channel_layouts=stereo,loudnorm=I=-18:TP=-2,aresample=48000,asetpts=N/SR/TB,atrim=0:$len,afade=t=out:st=$(python3 -c "print($len-0.1)"):d=0.1,adelay=$d|$d[v$idx];"
  labels+="[v$idx]"; idx=$((idx + 1))
  a=$(python3 -c "print(round($start-0.2-$RAMP,3))"); b=$(python3 -c "print(round($start+$len+0.3+$RAMP,3))")
  w+="+(st(0\\,clip((t-$a)/$RAMP\\,0\\,1))*0+ld(0)*ld(0)*(3-2*ld(0)))*(st(1\\,clip(($b-t)/$RAMP\\,0\\,1))*0+ld(1)*ld(1)*(3-2*ld(1)))"
done
f+="${labels}amix=inputs=${#NARR[@]}:normalize=0[narr];"
f+="[mus]volume=eval=frame:volume='1-(1-$DUCK)*clip(0${w}\\,0\\,1)'[bed];"
f+="[bed][narr]amix=inputs=2:normalize=0,loudnorm=I=-14:TP=-1.5:LRA=11,apad,atrim=0:$LEN[out]"
ffmpeg -v error -y "${inputs[@]}" -filter_complex "$f" -map "[out]" -ar 48000 -b:a 192k mix.mp3
