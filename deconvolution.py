import numpy as np

from scipy.signal import fftconvolve

from sine_sweep import sine_sweep

DELTA_PEAK_START = 150
DELTA_PEAK_DURATION = 300


def deconvolve(systemOutput, invfilter, Lp):
    numChans = systemOutput.shape[1]
    tmplen = invfilter.shape[0] + Lp-1
    RIRs = np.zeros(shape=(tmplen, numChans))

    for idx in range(0, numChans):
        currentChannel = systemOutput[:, idx]

        # Average over the repetitions - DEPRECATED. Should not be done.
        sig_reshaped = currentChannel.reshape(
            (1, Lp))
        sig_avg = np.mean(sig_reshaped, axis=0)

        # Deconvolution
        RIRs[:, idx] = fftconvolve(invfilter, sig_avg)

    return RIRs


def test_deconvolution(args):
    fs = args.fs
    duration = args.duration
    amplitude = args.amplitude
    padsilence = args.padsilence
    sweeprange = args.sweeprange

    sinsweep, inverse_sweep, padded_duration = sine_sweep(
        fs, duration, amplitude,
        min_freq_in_hz=sweeprange[0], max_freq_in_hz=sweeprange[1],
        pad_duration_in_seconds=padsilence
    )

    deltapeak = deconvolve(sinsweep, inverse_sweep, padded_duration)
    startid = duration*fs + padsilence*fs - DELTA_PEAK_START
    deltapeak = deltapeak[startid:startid + DELTA_PEAK_DURATION]

    return deltapeak
