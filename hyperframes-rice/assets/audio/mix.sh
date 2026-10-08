#!/bin/bash
# Builds mix.mp3 for the rice festival reel: the 128 BPM dance track (music3.mp3) with the
# narrator and Babari lines on the caption bars. The music eases down to
# DUCK of its level under each line (smoothstep ramps: ATTACK before, RELEASE after),
# then the whole mix is normalised for Instagram.
set -euo pipefail
cd "$(dirname "$0")"
# `./mix.sh b` builds mix-b.mp3 for variant B, which swaps in the "1년 준비" line (v4b).
# B also has its own leader clip, whose mouth opens at 4.08 s.
V2="v2.wav 4.14 1.39"; V4="v4.wav 11.35 2.68"; OUT=mix.mp3
if [ "${1:-a}" = b ]; then V2="v2.wav 4.08 1.39"; V4="v4b.wav 11.35 2.2"; OUT=mix-b.mp3; fi
# `./mix.sh c` is B with a cuter Babari: the same lines pitched up 4 semitones (v*c.wav,
# duration unchanged so the lip sync still lines up).
# B and C use the brighter narrator Jiwoo (n1j/n7j); A keeps Ha-Rin.
N1="n1-tight.wav 0.15 3.75"; N7="n7-tight.wav 22.64 6.75"
case "${1:-a}" in b | c) N1="n1j-tight.wav 0.12 3.84"; N7="n7j-tight.wav 22.55 7.1" ;; esac
C=""
if [ "${1:-a}" = c ]; then C=c; V2="v2c.wav 4.08 1.39"; V4="v4bc.wav 11.35 2.2"; OUT=mix-c.mp3; fi
LEN=30.0
# music3.mp3 is mastered at about -14 LUFS; 0.26 keeps it well under the voices.
GAIN=0.26
DUCK=0.4
ATTACK=0.35
RELEASE=0.6
# voice: file start(s) speech-length(s). n1/n7 are the off-screen narrator (Ha-Rin);
# v2-v6 are Babari (Ji-Hoon). v2 and v5/v6 are lip-synced inside the leader and
# close-up clips (clip starts 0 and 15.0) where the mouths open (4.14; 1.65 and 4.85),
# so their clip-local offsets are fixed.
# n1-tight/n7-tight are n1/n7.mp3 with their pauses shortened (n7 also 5% faster);
# n1j-tight/n7j-tight do the same for Jiwoo's takes (8% / 5% faster);
# v*.wav are the v*.mp3 lines with the trailing silence cut.
VOICE=("$N1" "$V2" "v3$C.wav 7.62 1.4" "$V4"
       "v5$C.wav 16.65 1.41" "v6$C.wav 19.85 1.07" "$N7")

inputs=(-i music3.mp3)
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
filters="[0:a]aformat=sample_rates=48000:channel_layouts=stereo,atrim=0:$LEN,volume=$GAIN,afade=t=out:st=$(python3 -c "print($LEN-1.5)"):d=1.5,volume=eval=frame:volume='1-(1-$DUCK)*$s*$s*(3-2*$s)'[bed];"
filters+="${labels}${vl}amix=inputs=${#VOICE[@]}:normalize=0[voice];"
filters+="[bed][voice]amix=inputs=2:normalize=0,loudnorm=I=-14:TP=-1.5:LRA=11,atrim=0:$LEN[out]"
ffmpeg -v error -y "${inputs[@]}" -filter_complex "$filters" -map "[out]" -ar 48000 -b:a 192k $OUT
