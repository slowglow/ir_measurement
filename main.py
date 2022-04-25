# ================================================================
# Room impulse response measurement with an exponential sine sweep
# ----------------------------------------------------------------
# Author:                    Maja Taseska, ESAT-STADIUS, KU LEUVEN
# ================================================================
import sounddevice as sd
from matplotlib import pyplot as plt

# modules from this software
import parser

from deconvolution import deconvolve, test_deconvolution
from recording import record, saverecording
from settings import LEN_RIR_IN_SECS
from sine_sweep import sine_sweep


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


def measure_ir(args):
    # 1. Create a test signal object, and generate the excitation

    sinsweep, inverse_sweep, padded_duration = sine_sweep(
        args.fs, args.duration, args.amplitude,
        min_freq_in_hz=args.sweeprange[0], max_freq_in_hz=args.sweeprange[1],
        pad_duration_in_seconds=args.padsilence
    )

    # 2. Record
    recorded = record(
        sinsweep, args.fs, args.inputdevice, args.outputdevice,
        args.inputChannelMap, args.outputChannelMap)

    # 3. Deconvolve
    rir = deconvolve(recorded, inverse_sweep, padded_duration)

    # 3.1 Truncate
    startId = sinsweep.shape[0] - args.padsilence*args.fs - 1
    endId = startId + int(LEN_RIR_IN_SECS*args.fs)
    # save some more samples before linear part to check for nonlinearities
    startIdToSave = startId - int(args.fs/2)
    rir_to_save = rir[startIdToSave:endId, :]
    rir = rir[startId:endId, :]

    return rir, rir_to_save, sinsweep, recorded


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
        rir, rir_to_save, sinsweep, recorded = measure_ir(args)
        saverecording(rir, rir_to_save, sinsweep, recorded, args.fs)


if __name__ == "__main__":
    main()
