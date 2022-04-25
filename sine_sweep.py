import numpy as np
from scipy import signal

from settings import EPS


def sine_sweep(fs, duration, amplitude,
               min_freq_in_hz=1,
               max_freq_in_hz=None,
               pad_duration_in_seconds=1):
    
    # Sweep till Nyquist to avoid ringing
    if max_freq_in_hz is None:
        max_freq_in_hz = int(fs/2)

    w1 = 2*np.pi*min_freq_in_hz/fs     # start of sweep in rad/sample
    w2 = 2*np.pi*max_freq_in_hz/fs     # end of sweep in rad/sample

    num_samples = duration*fs
    sinsweep = np.zeros(shape=(num_samples, 1))
    #time_steps = np.arange(0, 1, num_samples)/(num_samples-1)
    time_steps = np.linspace(0, 1, num_samples)

    # for exponential sine sweeping
    lw = np.log(w2/w1)
    sinsweep = amplitude * \
        np.sin(w1*(num_samples-1)/lw * (np.exp(time_steps*lw)-1))

    sinsweep = _fade_at_last_zero_crossing(sinsweep)
    inverse_sweep = _invert_sine_sweep(sinsweep, amplitude, w1, w2)
    sinsweep = _fade_in(sinsweep)
    sinsweep = _pad(sinsweep, pad_duration_in_seconds, fs)

    padded_duration = (2*pad_duration_in_seconds + duration)*fs

    return sinsweep, inverse_sweep, padded_duration


def _fade_in(sinsweep):
    # fade-in window. Fade out removed because causes ringing - cropping at zero cross instead
    num_samples = sinsweep.shape[0]
    taperStart = signal.tukey(num_samples, 0)
    taperWindow = np.ones(shape=(num_samples,))
    taperWindow[0:int(num_samples/2)] = taperStart[0:int(num_samples/2)]
    sinsweep = sinsweep*taperWindow

    return sinsweep


def _fade_at_last_zero_crossing(sinsweep):
    # Find the last zero crossing to avoid the need for fadeout
    # Comment the whole block to remove this

    # To my understanding this function is inverting the signal to search for the first 
    # zero instead of searching for it backwards, which would remove the 
    # need for inverting the signal and make it more readable.
    num_samples = sinsweep.shape[0]

    k = np.flipud(sinsweep)
    error = 1
    counter = 0
    while error > EPS:
        error = np.abs(k[counter])
        counter = counter+1

    k = k[counter::]
    sinsweep_hat = np.flipud(k)
    sinsweep = np.zeros(shape=(num_samples,))
    sinsweep[0:sinsweep_hat.shape[0]] = sinsweep_hat
    return sinsweep
    

def _invert_sine_sweep(sinsweep, amplitude, w1, w2):
    num_samples = sinsweep.shape[0]
    time_steps = np.linspace(0, 1, num_samples)

    envelope = (w2/w1)**(-time_steps)  # Holters2009, Eq.(9)
    invfilter = np.flipud(sinsweep)*envelope
    scaling = np.pi*num_samples * \
        (w1/w2-1)/(2*(w2-w1)*np.log(w1/w2)) * \
        (w2-w1)/np.pi  # Holters2009, Eq.10

    return invfilter/amplitude**2/scaling


def _pad(sinsweep, pad_duration_in_seconds, fs):
    # Final excitation including repetition and pauses
    sinsweep = np.expand_dims(sinsweep, axis=1)
    zerostart = np.zeros(shape=(pad_duration_in_seconds*fs, 1))
    zeroend = np.zeros(shape=(pad_duration_in_seconds*fs, 1))
    sinsweep = np.concatenate(
        (np.concatenate((zerostart, sinsweep), axis=0), zeroend), axis=0)
    
    # Remove this line when you are confident
    sinsweep = np.transpose(
        np.tile(np.transpose(sinsweep), 1))

    return sinsweep
