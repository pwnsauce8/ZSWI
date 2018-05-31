"""
Jednoduchá vizualizace EEG a EMG dat z XDF souboru v pythonu
Autor: Roman Kalivoda

požadavky:  Python 3.x
            xdf.py
            numpy
            matplotlib
            
"""
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from matplotlib.font_manager import FontProperties
from xdf import load_xdf

def add_markers():
    global marker
    for marker in range(len(markers["time_stamps"])):
        if str(markers["time_series"][marker]) == "['S  1']":
            plt.axvline(x=markers["time_stamps"][marker], label="S1", color='r', lw=0.5)
        else:
            plt.axvline(x=markers["time_stamps"][marker], label="S1", color='g', lw=0.5)


stream_file = input("Zadejte název xdf souboru:")

streams, header = load_xdf(stream_file)
eeg = None
emg = None
markers = None

# identifikace jednotlivych streamu
for stream in range(len(streams)):
    type = streams[stream]["info"]["type"][0]
    if type == 'EEG':
        eeg = streams[stream]
    elif type == 'EMG':
        emg = streams[stream]
    elif type == 'Markers':
        markers = streams[stream]
    

print("\nGeneruji graf...")
channel_count = int(eeg["info"]["channel_count"][0])
channels = [[] for _ in range(channel_count)]
for ch in range(channel_count):
    for serie in range(len(eeg["time_series"])):
        channels[ch].append(eeg["time_series"][serie][ch])
        
fig = plt.figure()
axes = []
rows = 30

# prvni EEG. Musi byt oddelene aby na nej mohli byt navazany ostatni osy
axes.append(plt.subplot2grid((rows, 1), (0, 0)))
plt.plot(eeg["time_stamps"], channels[0])
axes[0].set_ylabel(eeg["info"]["desc"][0]["channels"][0]["channel"][0]["label"][0])
axes[0].spines['right'].set_color('none')
axes[0].spines['top'].set_color('none')
plt.setp(axes[0].get_xticklabels(), visible=False)




add_markers()



for ch in range(1, channel_count):
    axes.append(plt.subplot2grid((rows, 1), (ch, 0), sharex=axes[0], sharey=axes[0]))
    plt.plot(eeg["time_stamps"], channels[ch])
    axes[ch].set_ylabel(eeg["info"]["desc"][0]["channels"][0]["channel"][ch]["label"][0])
    axes[ch].spines['right'].set_color('none')
    axes[ch].spines['top'].set_color('none')
    axes[ch].spines['bottom'].set_position('center')
    plt.setp(axes[ch].get_xticklabels(), visible=False)
    
    add_markers()

#EMG
pos = channel_count + 1
axes.append(plt.subplot2grid((rows, 1), (pos, 0), rowspan=rows - channel_count, sharex=axes[0]))
plt.plot(streams[2]["time_stamps"], streams[2]["time_series"], label="EMG")
axes[pos - 1].set_ylabel("EMG")
axes[pos - 1].spines['right'].set_color('none')
axes[pos - 1].spines['top'].set_color('none')

add_markers()

#vytvoreni legendy markeru
fontP = FontProperties()
fontP.set_size('small')
custom_lines = [Line2D([0], [0], color='r', lw=4),
                Line2D([0], [0], color='g', lw=4)]
plt.legend(custom_lines, ['S1', 'S2'], loc='lower right', prop=fontP)

plt.tight_layout()
# maximize window
fig_manager = plt.get_current_fig_manager()
fig_manager.set_window_title("Visualize v2")
if hasattr(fig_manager, 'window'):
    fig_manager.window.state('zoomed')
fig.show()
