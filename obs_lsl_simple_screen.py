import obspython as obs
from pylsl import StreamInfo, StreamOutlet
import time

# Global settings
source_name = "MYOBS"
refresh_rate = 0.1      # [sec]
lsl_refresh_rate = 5    # [sec]
curr_unix_ms = int(time.perf_counter_ns() * 1e-6)

info = StreamInfo(name="OBS-Timestamp-Screen",
                  type="timestamp",
                  channel_count=1,
                  nominal_srate=1/lsl_refresh_rate,
                  channel_format='int32',
                  source_id='obs-ts-screen')
outlet = StreamOutlet(info)

def script_description():
    return "A script to overlay the current time on the screen in OBS and push timestamp through LSL."

def script_update(settings):
    """Update the settings when changed in the UI."""
    global source_name, refresh_rate
    source_name = obs.obs_data_get_string(settings, "source_name")
    refresh_rate = obs.obs_data_get_double(settings, "refresh_rate")

    obs.timer_remove(update_time)  # Remove any existing timer
    obs.timer_remove(update_lsl)
    if source_name:
        obs.timer_add(update_time, int(refresh_rate * 1000))
        obs.timer_add(update_lsl, lsl_refresh_rate * 1000)

def script_defaults(settings):
    """Set default values for the script."""
    obs.obs_data_set_default_string(settings, "source_name", source_name)
    obs.obs_data_set_default_double(settings, "refresh_rate", refresh_rate)

def script_properties():
    """Define script properties for the UI."""
    props = obs.obs_properties_create()

    obs.obs_properties_add_text(props, "source_name", "Text Source Name", obs.OBS_TEXT_DEFAULT)
    # obs.obs_properties_add_int(props, "refresh_rate", "Refresh Rate (seconds)", 1, 60, 1)

    return props

def update_time():
    """Update the text source with the current time."""
    global curr_unix_ms
    if not source_name:
        return

    source = obs.obs_get_source_by_name(source_name)
    if source:
        curr_unix = time.perf_counter_ns()
        curr_unix_ms = int(curr_unix * 1e-6)

        settings = obs.obs_data_create()

        obs.obs_data_set_string(settings, "text", f"{curr_unix_ms}")
        obs.obs_source_update(source, settings)
        
        obs.obs_data_release(settings)
        obs.obs_source_release(source)

def update_lsl():
    outlet.push_sample([curr_unix_ms])
