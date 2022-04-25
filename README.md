# Impulse response measuring tool

#### Measuring room impulse responses with ```python``` and ```sounddevice```

This code is largely based on `pyrirtool` developed by  [Maja Taseska](https://github.com/maj4e) at [KU Leuven, ESAT-STADIUS](https://www.esat.kuleuven.be/stadius/).

The code is based on the exponential sine sweep method and its modifications, proposed by A. Farina [1, 2]. The python package [```sounddevice```](https://python-sounddevice.readthedocs.io/en/0.3.12/) is used for recording and playback.

I did mainly aesthetic modifications to the code to improve my own understanding of the measurement procedure.

For example, I am storing the configuration on a .json file instead of a .npy binary, which I think makes things more readable.
I have also transformed the "stimulus.py" file into two files: "sine_sweep.py" and "deconvolution.py".


### First steps
The main file used to record a room impulse response is ```main.py```. When running  it for the first time from the terminal, a file with default parameters is created in ```_data/config.npy``` (recording doesn't take place when running the script for the first time.)
```
=> python main.py
Default settings not detected. Creating a config file in _data
```

After default settings have been generated, they can be checked by typing
```
python main.py --config
```
The output should be (the different parameters will be explained later)
```
amplitude => 0.2
duration => 10
padsilence => 1
reps => 1
fs => 44100
inputChannelMap => [1]
outputChannelMap => [1]
inputdevice => 0
outputdevice => 1
sweeprange => [0, 0]
```


### Configuration from the command line

Some of the measurement settings can be passed as command line parameters. To see available options type
```
python main.py --help
```

#### Selecting the audio device
To see a list of available input and output devices, with the corresponding number of input and output channels type ```python main.py --listdev``` in the terminal. The output looks something like this:
```
=> python main.py --listdev
> 0 MacBook Pro Microphone, Core Audio (1 in, 0 out)
< 1 MacBook Pro Speakers, Core Audio (0 in, 2 out)
Default input and output device:  [0, 1]

```
If there are other devices available they should appear in the list as well. Then, desired input/output devices can be selected using their corresponding number in the list, and the keywords ```-indev``` (for input device) and ```-outdev``` (for output device). For example:
```
python main.py --setdev -indev 0 -outdev 1
```

## Measuring a room impulse response

To start a recording from the command line with custom parameters, type:
```
python main.py -dur 2 -r 2 -a 0.5 -ss 2 -es 1 -chin 1  -chou 2
```

  - Setting the sine sweep duration to 2 seconds: ```-dur 2```

  - Setting the sweep amplitude:  ```-a 0.5```
  - Setting the silence at the start and at the end of a sweep (e.g., 2 seconds and 1 second, respectively):  ```-ss 2 -es 1```

  -  Setting the input and output channels (for example to channel 1 and channel 2, respectively) ```-chin 1 -chou 2```

-  One can also record multiple channels simultaneously, for instance by setting ```-chin 1 2 3``` (if the channels are available). The number of available channels can be seen by typing ```main.py --listdev```






## References


[1] A. Farina, *Simultaneous Measurement of Impulse Response and Distortion with a Swept-Sine Technique*, 108th Audio Engineering Society Convention, 2000

[2] A. Farina, *Advancements in impulse response measurements by sine sweeps*, 122nd Audio Engineering Society Convention, 2007


## Authors

`pyrirtool` developed by  [Maja Taseska](https://github.com/maj4e) at [KU Leuven, ESAT-STADIUS](https://www.esat.kuleuven.be/stadius/).



## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details
