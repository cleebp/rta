# Real-time analysis
Playing around with on-board audio capture, analysis, and visualization in python.

## Requirements
- Mac osx
- Homebrew
- Python `>=3.6`
- iShowU Audio Capture (see below)


## Setup
**On mac with homebrew installed:**
- `brew install portaudio`
- `python3 -m venv venv`
- `source venv/bin/activate`
- `pip install -r requirements.txt`

**Next install iShowU Audio Capture and setup a virtual audio route:**
- Follow the install instructions from the latest [release](https://support.shinywhitebox.com/hc/en-us/articles/204161459-Installing-iShowU-Audio-Capture)
  - Be sure to allow the developer in your security preferences in the last step, this is a second allow after entering your password in the `.pkg` install
- Open the native mac app `Audio MIDI Setup`
- Click the `+` in the bottom left corner
- Setup your new audio route by clicking the checkboxes next to iShowU and Built-in Output
  - If you don't see iShowU then something went wrong in the install process
  - Make sure to select drift correction for both sources
  - Make sure both sources are at the same sample rate by switching the master device, this script assumes `96.0 kHz`
  - Your final master device should be built-in output
  - Optionally rename the new virtual audio route to something recognizable like `loopback`
- After your iShowU loopback is created set the `INPUT_DEVICE_INDEX` in `config.py`
  - Run `python helpers.py` to list your device indexes

## To Run
`cd rta/src`

`python stream.py`

Play some music ^.^