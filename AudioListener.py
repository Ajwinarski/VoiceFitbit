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

    def __init__(self):
        def int_or_str(text):
            """Helper function for argument parsing."""
            try:
                return int(text)
            except ValueError:
                return text

        #Global Variables
        self.parser = argparse.ArgumentParser(description=__doc__)
        self.parser.add_argument('-l', '--list-devices', action='store_true',
                            help='show list of audio devices and exit')
        self.parser.add_argument('-d', '--device', type=int_or_str,
                            help='input device (numeric ID or substring)')
        self.parser.add_argument('-r', '--samplerate', type=int, help='sampling rate')
        self.parser.add_argument('-c', '--channels', type=int, default=1, help='number of input channels')
        self.parser.add_argument('filename', nargs='?', metavar='FILENAME',
                            help='audio file to store recording to')
        self.parser.add_argument('-t', '--subtype', type=str, help='sound file subtype (e.g. "PCM_24")')
        self.args = self.parser.parse_args()
        self.args.filename = tempfile.mktemp(prefix=time.strftime("%d%m%Y-%S%M%H"),
                                        suffix='.wav', dir='./Audio/')

        self.recording = False

        if self.args.list_devices:
            print(sd.query_devices())
            self.parser.exit(0)
        if self.args.samplerate is None:
            device_info = sd.query_devices(self.args.device, 'input')
            # soundfile expects an int, sounddevice provides a float:
            self.args.samplerate = int(device_info['default_samplerate'])


    def begin(self):
        q = queue.Queue()
        self.args.filename = tempfile.mktemp(prefix=time.strftime("%d%m%Y-%S%M%H"),
                                        suffix='.wav', dir='./Audio/')

        def callback(indata, frames, time, status):
            """This is called (from a separate thread) for each audio block."""
            if status:
                print(status, file=sys.stderr)
            q.put(indata.copy())

        with sf.SoundFile(self.args.filename, mode='x', samplerate=self.args.samplerate,
                            channels=self.args.channels, subtype=self.args.subtype) as file:
            with sd.InputStream(samplerate=self.args.samplerate, device=0,
                                channels=self.args.channels, callback=callback):
                print("Recording audio.")
                while True:
                    state = GPIO.input(BUTTON)
                    while not state:
                        file.write(q.get())
                    self.end()

    def end(self):
        print('\nRecording finished: ' + repr(self.args.filename))
        pass


if __name__ == "__main__":

    BUTTON = 17
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(BUTTON, GPIO.IN)

    r = Recorder()
    print("Press button to begin recording.")
    # runs until Ctrl-C is pressed or an exception is had
    while True:
        state = GPIO.input(BUTTON)
        try:
            # Wait for user to click button
            while not state:
                time.sleep(0.4)
            r.begin()
            #print("closed")

        except KeyboardInterrupt:
            print('\nRecording finished: ' + repr(r.args.filename))
            r.parser.exit(0)
        except Exception as e:
            r.parser.exit(type(e).__name__ + ': ' + str(e))
