# OBS_LSL_bridge

## Installation

- Prerequisites
  - Install [OBS studio](https://obsproject.com/)
  - Valid python installation (e.g., `conda`)
  - Download `obs_lsl.py` from this repository


### Python environment setup

#### Windows and Linux

- Set dedicated conda environment for OBS
  - (Recomended) Create a new conda environment for OBS scripting
    - `conda create -n obs python=3.12`
  - Activate the environment and install `pylsl`
    - `conda activate obs`
    - `pip install pylsl` or using conda install

#### MacOS

> It is observed that OBS studio (30.2.3) does not recognize any conda environment or virtualenv. The following is a workaround where `pylsl` is installed on system python, which could result in some break in system dependency. Please use it as your own risk.

- Install [homebrew](https://brew.sh/)
- Using homebrew
  - install python 3.12: `brew install python@3.12`
  - install lab streaming layer: `brew install labstreaminglayer/tap/lsl`
- Install `pylsl`
  - `python3.12 -m pip install --break-system-packages pylsl`

### OBS configuration

- Config python scripting in OBS studio 
  - In OBS studio, navigate to `Tools -> Scripts -> Python Settings`
  - Select valid python installation path. E.g.,
    - Windows: `C:/Users/<username>/miniconda3/envs/obs` if conda env is used
    - MacOS: `/usr/local/Cellar/python#3.12/3.12.4/Frameworks` if using homebrew
      - the path is not directly accessible in Finder, use "Command + shift + G" and type in the directory
  - A message `"Loaded Python Version:3.12"` will be displayed if the path is correctly set
- Load `OBS-LSL bridge` script
  - Navigate to `Tools -> Scripts -> Scripts`, select "add" icon
  - Select `obs_lsl.py` downloaded from the previous step
- Activate time overlay on canvas
  - Add a new test source by `Sources -> + -> Text (GDI+)`
  - Name the source as `MYOBS`
    - Note the source must be named exactly `MYOBS` in order to have the script works
  - Change the display properties as needed and select OK
- Timestamp should be displayed on the screen, happy recording!

