# ================================================================
# Room impulse response measurement with an exponential sine sweep
# ----------------------------------------------------------------
# Author:                    Maja Taseska, ESAT-STADIUS, KU LEUVEN
# ================================================================
import sounddevice as sd
from matplotlib import pyplot as plt

# modules from this software
import parser

from stimulus import Stimulus, test_deconvolution
from recording import record, saverecording
from settings import LEN_RIR_IN_SECS

def list_devices():
    print(sd.query_devices())
    sd.check_input_settings()
    sd.check_output_settings()
    print("Default input and output device: ", sd.default.device)


def set_devices(args):
    sd.default.device[0] = args.inputdevice
    sd.default.device[1] = args.outputdevice
    sd.check_input_settings()
    sd.check_output_settings()
    print(sd.query_devices())
    parser.set_config(args)
    print("Default input and output device: ", sd.default.device)
    print("Sucessfully selected audio devices. Ready to record.")


def record_stimulus(args):
    # Create a test signal object, and generate the excitation
    testStimulus = Stimulus(args.fs)
    testStimulus.generate(args.fs, args.duration, args.amplitude,
                          args.startsilence, args.sweeprange)

    # Record
    recorded = record(
        testStimulus.signal, args.fs, args.inputdevice, args.outputdevice,
        args.inputChannelMap, args.outputChannelMap)

    # Deconvolve
    RIR = testStimulus.deconvolve(recorded)

    # Truncate
    startId = testStimulus.signal.shape[0] - args.endsilence*args.fs - 1
    endId = startId + int(LEN_RIR_IN_SECS*args.fs)
    # save some more samples before linear part to check for nonlinearities
    startIdToSave = startId - int(args.fs/2)
    RIRtoSave = RIR[startIdToSave:endId, :]
    RIR = RIR[startId:endId, :]

    # Save recordings and RIRs
    saverecording(RIR, RIRtoSave, testStimulus.signal, recorded, args.fs)


def main():
    # --- Parse command line arguments and check config
    flag_configInitialized = parser.check_config()
    if not flag_configInitialized:
        return

    args = parser.parse()
    parser.set_config(args)
    # -------------------------------

    if args.listdev == True:
        list_devices()
    elif args.setdev == True:
        set_devices(args)
    elif args.test == True:
        deltapeak = test_deconvolution(args)
        plt.plot(deltapeak)
        plt.show()
    else:
        record_stimulus(args)


if __name__ == "__main__":
    main()
