# %%
import pyxdf
import numpy as np

streams, info = pyxdf.load_xdf('test_recording.xdf')

obs = streams[0]

ts = obs['time_stamps']
data = np.array(obs['time_series'])

unix_time = data[:, 1].astype(int)

import matplotlib.pyplot as plt
plt.plot(ts, unix_time)