import pyaudio
import wave
from vad import VoiceActivityDetector
import json


def save_to_file(data, filename):
    with open(filename, 'w') as fp:
        json.dump(data, fp)

def create_wav(filename):
    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    RATE = 44100
    CHUNK = 1024
    RECORD_SECONDS = 2
    WAVE_OUTPUT_FILENAME = filename

    audio = pyaudio.PyAudio()

    # start Recording
    stream = audio.open(format=FORMAT, channels=CHANNELS,
                        rate=RATE, input=True,
                        frames_per_buffer=CHUNK)
                        #print "recording..."
    frames = []

    for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
        data = stream.read(CHUNK)
        frames.append(data)
        #print(data)

#print "finished recording"


    # stop Recording
    stream.stop_stream()
    stream.close()
    audio.terminate()

    waveFile = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
    waveFile.setnchannels(CHANNELS)
    waveFile.setsampwidth(audio.get_sample_size(FORMAT))
    waveFile.setframerate(RATE)
    waveFile.writeframes(b''.join(frames))
    waveFile.close()

if __name__ == "__main__":
    
    i = 0
    total_speech = 0
    try:
        while(True):
            speech_labels ={}
           
            if (i<4):

                i=i+1

            else:
                i=0;
            
            wav_name = 'file' + str(i) + '.wav'
            create_wav(wav_name)
            v = VoiceActivityDetector(wav_name)
            raw_detection = v.detect_speech()
            speech_labels, speech_in_wav = v.convert_windows_to_readible_labels(raw_detection)
            if (speech_in_wav>0.5):
                print ('we have speech in ' + wav_name);
            
            else:
                print ('we dont have speech in ' + wav_name);
            output_txt = 'testingreal'+str(i)+'.txt'
            total_speech = total_speech + speech_in_wav
            save_to_file(speech_labels, output_txt)
                
    except KeyboardInterrupt:
        print('Total time since program started:' + str(total_speech))
        print("Done")
