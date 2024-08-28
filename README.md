This project consists of Head-Related Transfer Function (HRTF) Convolution of a mono audio file, with a TKinter GUI component to provide the user the control over the position of the sound source in the auditory field using Tkinter. 

HRTFs are a form of mathematical representation of how an individual’s ear receives sound from a specific point in space. The different aspect of human body affects the way every sound is received by the human ear. The HRTFs used for this project are encoded in a SOFA format, which consists of a multidimensional arraywith each element represents the impulse response of a sound source at different positions.

The SOFA file used for this project is a Spherical Far-Field HRTF file recorded with a KU100 dummy head. The specifications for this file contain impulse responses for spherical system coordinates as follows:

Azimuth range: 0 to 360
Elevation range: -90 to 75
Radius: 1.2 m

Tkinter is employed to provide the user the control of changing the sliders for azimuth (in the increments of 10 degrees) and elevation (in the increments of 45 degrees).


<p align="center"><img width="495" alt="Screenshot 2024-08-28 at 5 37 13 PM" src="https://github.com/user-attachments/assets/3e354571-fe5c-4876-a330-a20a1253601c">
