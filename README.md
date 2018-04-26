# VoiceFitbit
Voice activity detection for wearable devices

## Sounddeive recording using RPi Zero W
### NOTE: You MUST run the following commands before beginning

sudo apt install libasound-dev portaudio19-dev libportaudio2 libportaudiocpp0 ffmpeg libav-tools 
sudo apt-get install python3-dev python3-venv 
python3 -m venv env 
env/bin/python -m pip install --upgrade pip setuptools
 
sudo nano /boot/config.txt
..* modify dtparam=audio=on to #dtparam=audio=on *
..* press Ctrl-X, then y, then hit enter

sudo nano /etc/asound.conf
..* modift the current pcm.dmixed to the following... *
....
....
...pcm.dmixed {
...  type dmix
...  slave {
...      pcm "hw:1,0"  # this depends on your input device (card,device)
...      period_time 0
...      period_size 1024
...      buffer_size 8192
...      rate 44100
...      format S16_LE
...  }
...  ipc_key 1024
...} 
....
....
..* press Ctrl-X, then y, then hit enter
 
pip3 install cffi
pip3 install numpy
pip3 install sounddevice

git clone https://github.com/respeaker/seeed-voicecard
cd seeed-voicecard
sudo ./install.py
sudo reboot
 
### after reboot you should be set to run sounddevice in python *

