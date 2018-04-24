#!/usr/bin/env python3

from matplotlib.animation import FuncAnimation
from time import sleep
import scipy.io.wavfile as wf
import matplotlib.pyplot as plt
from vad import VoiceActivityDetector
import numpy as np
import sounddevice as sd
import soundfile as sf
import argparse
import tempfile
import queue
import sys


def int_or_str(text):
    """Helper function for argument parsing."""
    try:
        return int(text)
    except ValueError:
        return text

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('-l', '--list-devices', action='store_true',
                    help='show list of audio devices and exit')
parser.add_argument('-d', '--device', type=int_or_str,
                    help='input device (numeric ID or substring)')
parser.add_argument('-w', '--window', type=float, default=200, metavar='DURATION',
                    help='visible time slot (default: %(default)s ms)')
parser.add_argument('-i', '--interval', type=float, default=30,
                    help='minimum time between plot updates (default: %(default)s ms)')
parser.add_argument('-b', '--blocksize', type=int, help='block size (in samples)')
parser.add_argument('-r', '--samplerate', type=float, help='sampling rate of audio device')
parser.add_argument('-n', '--downsample', type=int, default=10, metavar='N',
                    help='display every Nth sample (default: %(default)s)')
parser.add_argument('channels', type=int, default=[1], nargs='*', metavar='CHANNEL',
                    help='input channels to plot (default: the first)')

args = parser.parse_args()
if any(c < 1 for c in args.channels):
    parser.error('argument CHANNEL: must be >= 1')

mapping = [c - 1 for c in args.channels]            # Channel numbers start with 1
q = queue.Queue()                                   # life audio data queue
length = 882                                        # length of plot data window
plotdata = np.zeros((length, len(args.channels)))
fig, ax = plt.subplots()
lines = ax.plot(plotdata)
temp = True


#def


def update_plot(frame):
    """
    This is called by matplotlib for each plot update.

    Typically, audio callbacks happen more frequently than plot updates,
    therefore the queue tends to contain multiple blocks of audio data.
    """
    global plotdata, lines
    while True:
        try:
            data = q.get_nowait()
        except queue.Empty:
            break
        shift = len(data)
        plotdata = np.roll(plotdata, -shift, axis=0)
        plotdata[-shift:, :] = data
    for column, line in enumerate(lines):
        line.set_ydata(plotdata[:, column])
    return lines


def run():
    global length, plotdata, fig, ax, lines
    try:
        def audio_callback(indata, frames, time, status):
            """This is called (from a separate thread) for each audio block."""
            global temp
            if status:
                print(status, file=sys.stderr)
            # Fancy indexing with mapping creates a (necessary!) copy:
            if (temp):
                print("Frames: ",frames)
                print("Rate: ",args.samplerate)
                print("Time: ",time)
                print("Data type: ", type(indata))
                #print("Status: ",status)
                temp = False
            q.put(indata[::args.downsample, mapping])

        if args.list_devices:
            print(sd.query_devices())
            parser.exit(0)
        if args.samplerate is None:
            device_info = sd.query_devices(args.device, 'input')
            args.samplerate = device_info['default_samplerate']

        if len(args.channels) > 1:
            ax.legend(['channel {}'.format(c) for c in args.channels],
                      loc='lower left', ncol=len(args.channels))
        ax.axis((0, len(plotdata), -1, 1))
        ax.set_yticks([0])
        ax.yaxis.grid(True)
        ax.tick_params(bottom='off', top='off', labelbottom='off',
                     right='off', left='off', labelleft='off')
        fig.tight_layout(pad=0)

        stream = sd.InputStream(blocksize=512,
                                device=args.device,
                                channels=max(args.channels),
                                samplerate=40000,
                                callback=audio_callback)
        ani = FuncAnimation(fig, update_plot, interval=args.interval, blit=True)
        with stream:

            type(q)

            plt.show()
            #v = VoiceActivityDetector(stream, args.samplerate)
            #raw_detection = v.detect_speech()
            #speech_labels = v.convert_windows_to_readible_labels(raw_detection)
            #save_to_file(speech_labels, args.outputfile)

    except KeyboardInterrupt:
        print('\nRecording finished.')
        parser.exit(0)
    except Exception as e:
        parser.exit(type(e).__name__ + ': ' + str(e))


if __name__ == "__main__":
    run()
