# Mars Soil Sample Analysis

By Alec Suggs and Luke Wilson

05/12/2022

### INTRO

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

## DEPLOYMENT TO KUBERNETES

For our application database to be persistant with the ability to have python script workers running in the background we must use Kubernetes.
To deploy out system onto kubernetes, we must first ssh into a computer running kubernetes. We can do that on tacc as below
```bash
$ ssh <tacc_username>@isp02.tacc.utexas.edu
$ ssh <tacc_username>@coe332-k8s.tacc.cloud
```
Once we are here we can pull and deploy our system with:
```bash 
$ git clone https://github.com/lukewilson37/coe332-MarsSoilSampleAnalysis
$ kubectl apply -f kubernetes/prod
```
This will deploy the kubernetes files in ```kubernetes/prod``` onto the system.





