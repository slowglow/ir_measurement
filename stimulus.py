import numpy as np

from scipy.signal import fftconvolve

from sine_sweep import sine_sweep

class Stimulus:
    # Constructor
    def __init__(self, stimulusType, samplingRate):

        self.type = stimulusType
        self.fs = samplingRate
        self.Lp = []
        self.signal = []
        self.invfilter = []

    # Generate the stimulus and set requred attributes
    def generate(self, fs, duration, amplitude, silenceAtStart, silenceAtEnd, sweeprange):
        self.signal, self.invfilter, self.Lp = sine_sweep(
            fs, duration, amplitude, sweeprange[0], sweeprange[1], silenceAtStart)

    def deconvolve(self, systemOutput):
        numChans = systemOutput.shape[1]
        tmplen = self.invfilter.shape[0] + self.Lp-1
        RIRs = np.zeros(shape=(tmplen, numChans))

        for idx in range(0, numChans):
            currentChannel = systemOutput[:, idx]

            # Average over the repetitions - DEPRECATED. Should not be done.
            sig_reshaped = currentChannel.reshape(
                (1, self.Lp))
            sig_avg = np.mean(sig_reshaped, axis=0)

            # Deconvolution
            RIRs[:, idx] = fftconvolve(self.invfilter, sig_avg)

        return RIRs

# End of class definition
# ===========================================================================
# ===========================================================================
# NON-CLASS FUNCTIONS


def test_deconvolution(args):

    type = 'sinesweep'
    fs = args.fs
    duration = args.duration
    amplitude = args.amplitude
    silenceAtStart = args.startsilence
    silenceAtEnd = args.endsilence
    sweeprange = args.sweeprange

    # Create a test signal object, and generate the excitation
    testStimulus = Stimulus(type, fs)
    testStimulus.generate(fs, duration, amplitude,
                          silenceAtStart, silenceAtEnd, sweeprange)
    deltapeak = testStimulus.deconvolve(testStimulus.signal)
    startid = duration*fs + silenceAtStart*fs - 150
    deltapeak = deltapeak[startid:startid + 300]

    return deltapeak
