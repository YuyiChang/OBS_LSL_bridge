import obspython as obs
from datetime import datetime
from pylsl import StreamInfo, StreamOutlet
import time

# Global settings
source_name = "MYOBS"
time_format = "%m/%d/%y %H:%M:%S"
refresh_rate = 0.1  # Refresh every second

info = StreamInfo(name="OBS-Timestamp",
                  type="timestamp",
                  channel_count=1,
                  nominal_srate=30,
                  channel_format='int32',
                  source_id='obs-ts')
outlet = StreamOutlet(info)

def script_description():
    return "A script to overlay the current time on the screen in OBS."

def script_update(settings):
    """Update the settings when changed in the UI."""
    global source_name, time_format, refresh_rate
    source_name = obs.obs_data_get_string(settings, "source_name")
    time_format = obs.obs_data_get_string(settings, "time_format")
    refresh_rate = obs.obs_data_get_int(settings, "refresh_rate")

    obs.timer_remove(update_time)  # Remove any existing timer
    if source_name:
        obs.timer_add(update_time, refresh_rate * 1000)

def script_defaults(settings):
    """Set default values for the script."""
    obs.obs_data_set_default_string(settings, "source_name", source_name)
    obs.obs_data_set_default_string(settings, "time_format", time_format)
    obs.obs_data_set_default_double(settings, "refresh_rate", refresh_rate)

def script_properties():
    """Define script properties for the UI."""
    props = obs.obs_properties_create()

    obs.obs_properties_add_text(props, "source_name", "Text Source Name", obs.OBS_TEXT_DEFAULT)
    obs.obs_properties_add_text(props, "time_format", "Time Format (strftime)", obs.OBS_TEXT_DEFAULT)
    obs.obs_properties_add_float(props, "refresh_rate", "Refresh Rate (seconds)", 0.1, 60, 0.1)

    return props

def update_time():
    """Update the text source with the current time."""
    if not source_name:
        return

    source = obs.obs_get_source_by_name(source_name)
    if source:
        now = datetime.now()
        current_time = now.strftime(time_format)

        curr_unix = time.perf_counter_ns()
        curr_unix_ms = int(curr_unix * 1e-6)

        settings = obs.obs_data_create()

        outlet.push_sample([curr_unix_ms], curr_unix)
        # print(curr_unix_ms, curr_unix)

        display_txt = f"{current_time} - {curr_unix_ms}"

        obs.obs_data_set_string(settings, "text", display_txt)
        obs.obs_source_update(source, settings)
        
        obs.obs_data_release(settings)
        obs.obs_source_release(source)
