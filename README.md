# Pinel Localizer 

This repository provides the "Pinel localizer", a 5-minute functional magnetic resonance imaging (fMRI) stiumulation protocol which reliably captures the cerebral bases of key cognitive functions at an individual level, including auditory and visual perception, motor actions, reading, language comprehension, and mental calculation. 

Reference:

Pinel, P., Thirion, B., Meriaux, S., Jobert, A., Serres, J., Le Bihan, D., Poline, J.-B., & Dehaene, S. (2007). Fast reproducible identification and large-scale databasing of individual functional cognitive networks. _BMC Neuroscience_, 8(1), 91. https://doi.org/10.1186/1471-2202-8-91


The script `pinel_localizer.py` is based on https://github.com/chrplr/audiovis


## Prerequisites

The `pinel_localizer.py` script relies on the expyriment module (see [https://www.expyriment.org/](https://www.expyriment.org/)) which can be installed with:

    pip install expyriment


# hardware 

* A video screen or video projector 
* headphones for auditory stimuli
* Two response buttons, one for the left hand and one for the right hand, associated to 'b' and 'y' keypresses.
* The experiment waits for a 't' keypress event to start

## Running the protocol

First you must set three environment variables:

     export EXPYRIMENT_DISPLAY=0
     export EXPYRIMENT_DISPLAY_RESOLUTION=1920x1080
     export SUBJECT=10    # change to the correct value
 
Then you can launch the experiment through the menu:

     . menu_localizer.sh


Tihis will display the following dialog window:
![](./menu_dialog_localizer.png "menu_dialog_localizer.png")


At the end of the experiment, the details about the events can be found in the `data/*.xpd` files.

    
### Using the command line


To list the options:

    python pinel_localizer.py -h


The command for the localizer protocol with the options is:

    python pinel_localizer.py --background-color 0 0 0 --text-color 250 250 250 --rsvp-display-time=250 --rsvp-display-isi=100 --picture-display-time=200 --picture-isi=0 --fs_delay_time=100 --stim-dir stim_files  --total-duration=301000  --csv_file session1_localizer_standard.csv

The command for launching the instructions is:

    python pinel_localizer.py --background-color 0 0 0 --text-color 250 250 250 --rsvp-display-time=250 --rsvp-display-isi=100 --picture-display-time=200 --picture-isi=0 --fs_delay_time=100 --stim-dir stim_files  --total-duration=301000  --splash instructions_localizer.csv

The command for launching the calibration is:

    python pinel_localizer.py --background-color 0 0 0 --text-color 250 250 250 --rsvp-display-time=250 --rsvp-display-isi=100 --picture-display-time=200 --picture-isi=0 --fs_delay_time=100 --stim-dir stim_files  --total-duration=301000    --cali 1



The options for the localizer are: 

* --background-color 0 0 0 : color of the background
* --csv_file : file for stimulation
* --text-color 250 250 250 : color of the text
* --rsvp-display-time=250 : set the duration of display of single words in rsvp stimuli
* --rsvp-display-isi=100 : set the duration of display of single words in rsvp stimuli
* --picture-display-time=200 :  set the duration of display of pictures
* --picture-isi=0 : set the ISI between pictures in pictseq sequence
* --fs_delay_time=100 : time between the end of blanck screen and the beginning of fixation cross
* --stim-dir stim_files : directory in which stim are available
* --splash : csv file to propose the instructions
* --total-duration=301000 : all duration of the expyriment
* --cali : option to launch only the calibration




