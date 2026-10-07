#!/bin/bash
# Builds mix.mp3 for the ginseng reel: a 29 s section of the user's Suno track
# (music4.mp3, 132 BPM) with the narrator and leader ginseng lines on the caption bars.
# The music eases down to DUCK of its level under each line (smoothstep ramps:
# ATTACK before, RELEASE after), then the whole mix is normalised for Instagram.
set -euo pipefail
cd "$(dirname "$0")"
LEN=29.095
# The song's first drop is at 16.751 s; starting at 2.203 (a downbeat) puts it on
# bar 8 of the reel (14.548 s), where the close-up enters.
MUSIC_START=2.203
# music4.mp3 is mastered at about -15.6 LUFS; 0.28 keeps it well under the voices.
GAIN=0.28
DUCK=0.4
ATTACK=0.35
RELEASE=0.6
# voice: file start(s) speech-length(s). n1/n7 are the off-screen narrator (Ha-Rin);
# v2-v6 are the leader ginseng. v2 and v5/v6 are lip-synced inside the leader and
# close-up clips (clip starts 0 and 14.548), so their clip-local offsets are fixed.
# n1-tight.wav is n1.mp3 with its middle pause shortened and 10% faster.
VOICE=("n1-tight.wav 0.15 3.62" "v2.mp3 4.07 2.4" "v3.mp3 7.392 1.9" "v4.mp3 11.009 2.3"
       "v5.mp3 14.653 2.25" "v6.mp3 18.553 1.95" "n7.mp3 21.961 6.25")

inputs=(-i music4.mp3)
labels=""
windows=""
idx=1
for v in "${VOICE[@]}"; do
  read -r file start len <<<"$v"
  inputs+=(-i "$file")
  ms=$(python3 -c "print(int($start*1000))")
  labels+="[$idx:a]aformat=sample_rates=48000:channel_layouts=stereo,atrim=0:$len,afade=t=out:st=$(python3 -c "print($len-0.08)"):d=0.08,volume=1.6,adelay=$ms|$ms[v$idx];"
  a=$(python3 -c "print(round($start-0.1-$ATTACK,3))"); b=$(python3 -c "print(round($start+$len+0.1+$RELEASE,3))")
  windows+="+clip((t-$a)/$ATTACK\\,0\\,1)*clip(($b-t)/$RELEASE\\,0\\,1)"
  idx=$((idx + 1))
done
vl=""; for i in $(seq 1 ${#VOICE[@]}); do vl+="[v$i]"; done
# s = how far into a duck we are (0..1); smoothstep s*s*(3-2*s) makes the dips ease in and out.
s="clip(0${windows}\\,0\\,1)"
filters="[0:a]aformat=sample_rates=48000:channel_layouts=stereo,atrim=$MUSIC_START:$(python3 -c "print($MUSIC_START+$LEN)"),asetpts=PTS-STARTPTS,volume=$GAIN,afade=t=out:st=$(python3 -c "print($LEN-1.5)"):d=1.5,volume=eval=frame:volume='1-(1-$DUCK)*$s*$s*(3-2*$s)'[bed];"
filters+="${labels}${vl}amix=inputs=${#VOICE[@]}:normalize=0[voice];"
filters+="[bed][voice]amix=inputs=2:normalize=0,loudnorm=I=-14:TP=-1.5:LRA=11,atrim=0:$LEN[out]"
ffmpeg -v error -y "${inputs[@]}" -filter_complex "$filters" -map "[out]" -ar 48000 -b:a 192k mix.mp3
