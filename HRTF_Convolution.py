import tkinter as tk
import numpy as np
import scipy.signal as signal
import soundfile as sf
import sounddevice as sd
import sofa



def find_nearest(array, value):
    array = np.asarray(array)
    idx = (np.abs(array - value)).argmin()
    return array[idx], idx


HRTF_PATH = "/Users/shaun/Downloads/DSP/HRIR_FULL2DEG.sofa"
# Azimuth range = 0, 359
# Elevation range = -90 to 75
# radius = 1.2m



HRTF = sofa.Database.open(HRTF_PATH)

#print("Dimensions")
#HRTF.Dimensions.dump()
#
#print("Variables")
#HRTF.Variables.dump()
#
#print(sofa.access.Metadata(HRTF))

#print(sofa.conventions.implemented())

AUDIO_FILE_PATH = "/Users/shaun/Downloads/DSP/pingpong.wav"
audio_data, fs = sf.read(AUDIO_FILE_PATH)


source_positions = HRTF.Source.Position.get_values(system="spherical")
#print("Number of measurements: ", HRTF.Dimensions.N) 128
# positions format
# [az, el, rad]


root = tk.Tk()
root.title("Real-Time HRTF Audio Convolution")


def update_audio(azimuth_slider, elevation_slider, azimuth_label, elevation_label):
    actual_azimuth = azimuth_slider.get()
    actual_elevation = elevation_slider.get()
    update_labels(azimuth_label, elevation_label, actual_azimuth, actual_elevation)
    
    

# By default, if the azimuth value increase, it moves anticlockwise
# In order to make sure the azimuth moves clockwise, we mirror the angle by subtracting 360
    angle =  360 - actual_azimuth
    if angle == 360:
        angle = 0
    
    #print("Angle: ", angle)


    
    
    
    az, az_idx = find_nearest(source_positions[:, 0], angle)
    #print("Azimuth: ", az)
    subpositions = source_positions[np.where(source_positions[:, 0] == az)]
    el, sub_idx = find_nearest(subpositions[:, 1], actual_elevation)
    #print("Elevation: ", el)
    

    # Get HRTF data
    H = np.zeros([HRTF.Dimensions.N, 2])
    
    
    H[:, 0] = HRTF.Data.IR.get_values(indices={"M": az_idx + sub_idx, "R": 0, "E": 0})
    H[:, 1] = HRTF.Data.IR.get_values(indices={"M": az_idx + sub_idx, "R": 1, "E": 0})
    

    # Convolurion
    convolved_audio_L = signal.fftconvolve(audio_data, H[:, 0])
    convolved_audio_R = signal.fftconvolve(audio_data, H[:, 1])

    
    sd.play(np.column_stack([convolved_audio_L, convolved_audio_R]), fs)
    
def update_labels(azimuth_label, elevation_label, azimuth, elevation):
    azimuth_label.config(text=f"Azimuth: {azimuth:.2f} degrees")
    elevation_label.config(text=f"Elevation: {elevation:.2f} degrees")

# GUI labels and sliders
azimuth_label = tk.Label(root, text="Azimuth: 0 degrees")
elevation_label = tk.Label(root, text="Elevation: 0 degrees")
azimuth_label.pack()
elevation_label.pack()

azimuth_slider = tk.Scale(root, from_=0, to=360, resolution= 10, orient=tk.HORIZONTAL,
                          label="Azimuth Scale", command=lambda val: update_audio(azimuth_slider, elevation_slider, azimuth_label, elevation_label))
elevation_slider = tk.Scale(root, from_=-45, to=45, resolution=45, orient=tk.HORIZONTAL,
                            label="Elevation Scale", command=lambda val: update_audio(azimuth_slider, elevation_slider, azimuth_label, elevation_label))
azimuth_slider.pack()
elevation_slider.pack()


root.mainloop()
