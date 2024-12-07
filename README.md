# OBS_LSL_bridge

## Installation

- Prerequisites
  - Install [OBS studio](https://obsproject.com/)
  - Valid python installation (e.g., `conda`)
  - Download `obs_lsl.py` from this repository
- (Recomended) Set dedicated conda environment for OBS
  - Create a new conda environment for OBS scripting
    - `conda create -n obs python=3.12`
  - Activate the environment and install `pylsl`
    - `conda activate obs`
    - `pip install pylsl` or using conda install
- Config python scripting in OBS studio 
  - In OBS studio, navigate to `Tools -> Scripts -> Python Settings`
  - Select valid python installation path
    - e.g., `C:/Users/<username>/miniconda3/envs/obs` on windows if using conda env
  - A message `"Loaded Python Version:3.12"` will be displayed if the path is correctly set
- Load `OBS-LSL bridge` script
  - Navigate to `Tools -> Scripts -> Scripts`, select "add" icon
  - Select `obs_lsl.py` downloaded from the previous step
- Activate time overlay on canvas
  - Add a new test source by `Sources -> + -> Text (GDI+)`
  - Name the source as `MYOBS`
    - Note the source must be named exactly `MYOBS` in order to have the script works
  - Change the display properties as needed and select OK
- Timestamp should be displayed on the screen