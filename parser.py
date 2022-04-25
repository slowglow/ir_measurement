# ================================================================
# Parsing command line arguments
# ----------------------------------------------------------------
# Author:                    Maja Taseska, ESAT-STADIUS, KU LEUVEN
# ================================================================
import argparse
import os
import json

from settings import CONFIG_PATH, BASE_CONFIG


# === FUNCTION: Parsing command line arguments
def parse():
    # Load the config
    with open(CONFIG_PATH) as f:
        config = json.load(f)

    parser = argparse.ArgumentParser(description='Setting the parameters for RIR measurement using exponential sine sweep \n ----------------------------------------------------------------------')
    #---
    parser.add_argument("-f", "--fs", type = int, help=" The sampling rate (make sure it matches that of your audio interface). Default: 44100 Hz.", default = config['fs'])
    #---
    parser.add_argument("-dur", "--duration", type = int, help=" The duration of a single sweep. Default: 15 seconds.", default = config['duration'])
    #---
    # parser.add_argument("-fr", "--frange", type =  tuple, help = "Frequency range of the sweep (f_min, f_max). Default: (0.01,20000) Hz.", default = (0.01,20000))
    #---
    parser.add_argument("-a", "--amplitude", type = float, help = "Amplitude of the sine. Default: 0.7",default = config['amplitude'])
    #---
    parser.add_argument("-ss", "--padsilence", type = int, help = "Duration of silence at the start and end of a sweep, in seconds. Default: 1.", default = config['padsilence'])

    parser.add_argument("-frange", "--sweeprange", nargs='+', type=int, help = "Frequency range of the sweep", default = config['sweeprange'])
    #---
    parser.add_argument("-chin", "--inputChannelMap", nargs='+', type=int, help = "Input channel mapping", default = config['inputChannelMap'])

    parser.add_argument("-chou", "--outputChannelMap", nargs='+', type=int, help = "Output channel mapping", default = config['outputChannelMap'])


    #--- arguments for checking and selecting audio interface
    parser.add_argument("-outdev", "--outputdevice", type = int, help = "Output device ID.", default = config['outputdevice'])

    parser.add_argument("-indev", "--inputdevice", type = int, help = "Input device ID.",default = config['inputdevice'])

    parser.add_argument('--listdev', help='List the available devices, indicating the default one',action='store_true')

    parser.add_argument('--config', help = 'List the default measurement parameters (devices, channels, and signal properties)', action = 'store_true')

    parser.add_argument('--setdev', help='Use this keyword in order to change the default audio interface.',action='store_true')

    parser.add_argument('--test', help = 'Just for debugging: check the output of deconvolution applied directly to the computer-generated sinesweep', action='store_true')


    args = parser.parse_args()

    return args


#------------------------------------------------
# === FUNCTION: Update config

def set_config(args):

    if (args.listdev == False and  args.config == False):
        config = {
            "amplitude": args.amplitude,
            "duration" : args.duration,
            "padsilence": args.padsilence,
            "fs" : args.fs,
            "inputChannelMap" : args.inputChannelMap,
            "outputChannelMap": args.outputChannelMap,
            "inputdevice": args.inputdevice,
            "outputdevice": args.outputdevice,
            "sweeprange": args.sweeprange
        }

        with open(CONFIG_PATH, "w") as f:
            json.dump(config, f, indent=4)
        # np.save('_data/config.npy', config)
        print(config)


#-------------------------------------------------------------
# === FUNCTION: Check if a file with config exists. If not, make one

def check_config():

    flag_configInitialized = True

    if not os.path.exists('_data'):
        os.makedirs('_data')

    if not os.path.exists(CONFIG_PATH):
        print("Default settings not detected. Creating a config file in _data")

        with open(CONFIG_PATH, "w") as f:
            json.dump(BASE_CONFIG, f, indent=4)
        flag_configInitialized = False

    return flag_configInitialized
