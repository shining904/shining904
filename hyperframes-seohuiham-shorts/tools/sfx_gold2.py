# Synthesised sound design for the extended gold short: airy whooshes under each morph,
# a glassy shimmer when a shape lands, a deep boom with a long tail at the hit.
# Deterministic (seeded) so re-running reproduces the same file.
import sys
import numpy as np
from scipy.signal import butter, sosfilt, fftconvolve
from scipy.io import wavfile

SR, DUR = 44100, 37.5
rng = np.random.default_rng(11)
out = np.zeros((int(SR * DUR), 2))


def place(sig, t, gain=1.0, pan=0.0):
    i = int(t * SR)
    sig = sig[: len(out) - i]
    out[i:i + len(sig), 0] += sig * gain * (1 - max(0, pan))
    out[i:i + len(sig), 1] += sig * gain * (1 + min(0, pan))


def reverb(sig, secs=2.5, mix=0.35):
    n = int(SR * secs)
    ir = rng.standard_normal(n) * np.exp(-np.linspace(0, 7, n))
    wet = fftconvolve(sig, ir)[: len(sig) + n]
    wet /= np.max(np.abs(wet)) + 1e-9
    dry = np.concatenate([sig, np.zeros(len(wet) - len(sig))])
    return dry * (1 - mix) + wet * mix * np.max(np.abs(sig))


def whoosh(d=1.6):
    n = int(SR * d)
    noise = rng.standard_normal(n)
    out_ = np.zeros(n)
    # sweep a band-pass up then down by crossfading fixed bands
    bands = [250, 450, 800, 1400, 2400]
    pos = np.sin(np.linspace(0, np.pi, n)) * (len(bands) - 1)
    for k, f in enumerate(bands):
        sos = butter(2, [f * 0.7, f * 1.4], btype="band", fs=SR, output="sos")
        w = np.clip(1 - np.abs(pos - k), 0, 1)
        out_ += sosfilt(sos, noise) * w
    env = np.sin(np.linspace(0, np.pi, n)) ** 2
    return reverb(out_ * env / np.max(np.abs(out_ * env)), 1.2, 0.3)


def shimmer(d=2.2):
    n = int(SR * d)
    t = np.arange(n) / SR
    s = np.zeros(n)
    for k in range(9):
        f = rng.uniform(2200, 6500)
        t0 = rng.uniform(0, 0.35)
        e = np.where(t > t0, np.exp(-(t - t0) * rng.uniform(4, 8)), 0)
        s += np.sin(2 * np.pi * f * t) * e * rng.uniform(0.4, 1)
    return reverb(s / np.max(np.abs(s)), 2.0, 0.5)


def boom(d=4.0):
    n = int(SR * d)
    t = np.arange(n) / SR
    f = 32 + 48 * np.exp(-t * 6)
    body = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 1.4)
    sos = butter(2, 900, fs=SR, output="sos")
    hit = sosfilt(sos, rng.standard_normal(n)) * np.exp(-t * 18) * 0.8
    s = body + hit
    return reverb(s / np.max(np.abs(s)), 3.0, 0.3)


def riser(d=1.8):
    n = int(SR * d)
    sos = butter(2, [1500, 7000], btype="band", fs=SR, output="sos")
    s = sosfilt(sos, rng.standard_normal(n)) * np.linspace(0, 1, n) ** 3
    return s / np.max(np.abs(s))


for t0, pan in [(2.5, -0.3), (7.5, 0.3), (12.1, -0.3), (17.3, 0.3), (29.3, 0.0)]:
    place(whoosh(), t0, 0.5, pan)
for t0 in [4.3, 9.0, 13.7, 18.9, 33.8]:
    place(shimmer(), t0, 0.28)
place(riser(), 24.1 - 1.8, 0.25)
place(boom(), 24.08, 1.0)
place(shimmer(), 24.1, 0.35)
out /= np.max(np.abs(out)) * 1.05
wavfile.write(sys.argv[1], SR, (out * 32767).astype(np.int16))
