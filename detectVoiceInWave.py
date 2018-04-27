from vad import VoiceActivityDetector
import argparse
import json

def save_to_file(data, filename):
    with open(filename, 'w') as fp:
        json.dump(data, fp)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Analyze input wave-file and save detected speech interval to json file.')
   # parser.add_argument('inputfile', metavar='INPUTWAVE',
    #                    help='the full path to input wave file')
    parser.add_argument('outputfile', metavar='OUTPUTFILE',
                        help='the full path to output json file to save detected speech intervals')
    args = parser.parse_args()

    # Create a speech detection object and read in the audio data
    v = VoiceActivityDetector('FILE_NAME.wav')

    # Detect speech in the given data
    raw_detection = v.detect_speech()

    # Convert the detected speech signals to a readable format
    speech_labels = v.convert_windows_to_readible_labels(raw_detection)

    # Save the converted and detected speech to a file
    save_to_file(speech_labels, args.outputfile)
