#!/usr/bin/env python3
import RPi.GPIO as GPIO
import pixels as Pixels
import argparse
import tempfile
import time
import queue
import sys
import sounddevice as sd
import soundfile as sf


class Recorder():

    def int_or_str(text):
        """Helper function for argument parsing."""
        try:
            return int(text)
        except ValueError:
            return text

    #Global Variables
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('-l', '--list-devices', action='store_true',
                        help='show list of audio devices and exit')
    parser.add_argument('-d', '--device', type=int_or_str,
                        help='input device (numeric ID or substring)')
    parser.add_argument('-r', '--samplerate', type=int, help='sampling rate')
    parser.add_argument('-c', '--channels', type=int, default=1, help='number of input channels')
    parser.add_argument('filename', nargs='?', metavar='FILENAME',
                        help='audio file to store recording to')
    parser.add_argument('-t', '--subtype', type=str, help='sound file subtype (e.g. "PCM_24")')
    args = parser.parse_args()
    args.filename = tempfile.mkstemp(prefix=time.strftime("%d%m%Y-%S%M%H"),
                                    suffix='.wav', dir='')


    GPIO.setmode(GPIO.BCM)
    GPIO.setup(17, GPIO.IN)

    def __init__(self):
        global q, args, parser
        self.state = GPIO.input(17)     # BUTTON = 17
        self.recording = False
        if args.list_devices:
            print(sd.query_devices())
            parser.exit(0)
        if args.samplerate is None:
            device_info = sd.query_devices(args.device, 'input')
            # soundfile expects an int, sounddevice provides a float:
            args.samplerate = int(device_info['default_samplerate'])


    def record(self):
        # runs until Ctrl-C is pressed or an exception is had
        try:
            # Wait for user to click button
            print("Press button to begin recording.")
            while not self.state:
                time.sleep(0.1)
            begin()

        except KeyboardInterrupt:
            print('\nRecording finished: ' + repr(args.filename))
            parser.exit(0)
        except Exception as e:
            parser.exit(type(e).__name__ + ': ' + str(e))

    def begin(self):
        q = queue.Queue()
        args.filename = tempfile.mkstemp(prefix=time.strftime("%d%m%Y-%S%M%H"),
                                        suffix='.wav', dir='')

        def callback(indata, frames, time, status):
            """This is called (from a separate thread) for each audio block."""
            if status:
                print(status, file=sys.stderr)
            q.put(indata.copy())

        with sf.SoundFile(args.filename, mode='x', samplerate=args.samplerate,
                            channels=args.channels, subtype=args.subtype) as file:
            with sd.InputStream(samplerate=args.samplerate, device=0,
                                channels=args.channels, callback=callback):
                print("Recording audio.")
                while not self.state:
                    file.write(q.get())
                end()

    def end(self):
        print('\nRecording finished: ' + repr(args.filename))
        pass


if __name__ == "__main__":
    r = Recorder()

    while True:
        r.record()
