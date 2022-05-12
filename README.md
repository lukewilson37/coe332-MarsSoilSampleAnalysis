# Mars Soil Sample Analysis

#### INTRO

In 2011 NASA launched its Mars Science Labratory, otherwise know as Curiosity. Curiiosity was to go and study Mars soil and atmosphere.
One of the Instruments attatched to Curiosity was the Alpha Particle X-Ray Spectrometer ([APXS](https://mars.nasa.gov/msl/spacecraft/instruments/apxs/)). 
APXS was reponcible for analyzing the amounts of chemical elements in martian soil and rock samples. 
APSS is attatched to one of Curiosities arm, which would place it very close to a sample for analysis.
APXS as a result produced a lot of data which we will provide methods for analylizing in this project.
We will set up a database for holding this data and processing and storing analysis job requests and results.
We will have an assocaciated Flask application appended to the database from which one can read, create, update and delete data. 
Users will also have the approtunity to submit analysis jobs to the application.

## DOWNLOADING OF THE DATA

The data we will be analyzing can be found on [this page](https://pds-geosciences.wustl.edu/missions/msl/apxs.htm) or more specifically [here](https://pds-geosciences.wustl.edu/msl/msl-m-apxs-4_5-rdr-v1/mslapx_1xxx/data/). 
The data consists of directories for each sample the rover analyzed. 
Each Directory has a csv file containing the percentage of each element found in the sample. That is the csv file with "rwp" in it. 
The data is not easily retreivable, so we have to use an unconventional method. We first create a ```.txt``` file with the address of every csv file we need to access using:
```bash
$ wget -r -np -R "index.html*" https://pds-geosciences.wustl.edu/msl/msl-m-apxs-4_5-rdr-v1/mslapx_1xxx/data/
$ ls pds-geosciences.wustl.edu/msl/msl-m-apxs-4_5-rdr-v1/mslapx_1xxx/data/sol0*/*rwp*.csv > coe332-MarsSoilSampleAnalysis/initial_sol_list.txt 
```
This needs to be run in the same directory as our ```app.py``` script, so that script can easily pull from the list.

##
