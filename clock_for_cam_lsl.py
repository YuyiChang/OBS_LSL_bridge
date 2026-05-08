import obspython as obs
from datetime import datetime
from pylsl import StreamInfo, StreamOutlet
import time

# Global variables
source_name = ""
last_lsl_push_time = 0
outlet = None

def update_logic():
    global outlet, last_lsl_push_time
    
    source = obs.obs_get_source_by_name(source_name)
    if not source:
        return

    now = datetime.now()
    curr_unix_ns = time.time_ns()
    curr_unix_s = curr_unix_ns / 1e9
    curr_unix_ms = int(curr_unix_ns // 1_000_000)

    # 1. FORMAT TIME STRING (MM/DD/YYYY HH:MM:SS.milliseconds)
    # %f is microseconds, [:-3] trims it to milliseconds
    time_str = now.strftime("%m/%d/%Y %H:%M:%S.%f")[:-3]
    
    # Update OBS Screen (Every 10ms)
    settings = obs.obs_data_create()
    obs.obs_data_set_string(settings, "text", time_str)
    obs.obs_source_update(source, settings)
    obs.obs_data_release(settings)
    obs.obs_source_release(source)

    # 2. PUSH TO LSL (Every 10 seconds)
    if (curr_unix_s - last_lsl_push_time) >= 10.0:
        if outlet is None:
            # Create a 2-channel STRING stream
            # Channel 1: Human-readable time
            # Channel 2: Unix Timestamp (as string)
            info = StreamInfo('OBS-Studio', 'Timestamp', 2, 0.1, 'string', 'obs-001')
            outlet = StreamOutlet(info)
        
        # Push both pieces of data as a list of strings
        outlet.push_sample([time_str, str(curr_unix_ms)])
        
        last_lsl_push_time = curr_unix_s
        print(f"[LSL PUSH] {time_str} | Unix: {curr_unix_ms}")

def script_update(settings):
    global source_name
    source_name = obs.obs_data_get_string(settings, "source_name")

    obs.timer_remove(update_logic)
    if source_name:
        obs.timer_add(update_logic, 10)

def script_description():
    return "Display: MM/DD/YYYY HH:MM:SS.ms (10ms refresh)\nLSL: Pushes String + Unix MS every 10s"

def script_properties():
    props = obs.obs_properties_create()
    obs.obs_properties_add_text(props, "source_name", "Text Source Name", obs.OBS_TEXT_DEFAULT)
    return props

def script_defaults(settings):
    obs.obs_data_set_default_string(settings, "source_name", "MYOBS")