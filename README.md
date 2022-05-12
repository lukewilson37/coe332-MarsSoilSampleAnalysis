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
$ kubectl apply -f kubernetes/prod/mssa-prod-redis-pvc.yml
$ kubectl apply -f kubernetes/prod/mssa-prod-redis-deployment.yml
$ kubectl apply -f kubernetes/prod/mssa-prod-redis-service.yml
```
This will deploy the redis database onto the system. Once we have our database, we find out redis service address with:
```bash
$ kubectl get service
```
Here we find the IP address for our redis service. We copy that address into our flask ```.yml``` files.
```yaml
		env:
          - name: REDIS_IP
            value: 10.108.182.25
```
Now we are ready to deploy the flask application. We can do this more simply with
```bash
$ kubectl apply -f kubernete/prod/
```
Now our application in fully on kubernetes!

## RUNNING THE INTEGRATION TESTS

Running the Integration tests is very simple. The file has already been formated ans thus that is needed to to write
```bash
$ pytest
```
in the repository from the kubernetes computer.
The test will verify (1) the flaks app is running, (2) the redis database is operating (3) the CRUD operations work and (4) the worker is receiving and processing job requests.
This pytest follows typical pytest operations

## CRUD OPERATIONS

CRUD stands for Create, Read, Update and Delete. Our application offers all of there features!
Let us begin with read. We can run 
```bash
$ kubectl get service
```
again to find our flask IP address and port. Once these are obtained we can interact with our application using curl commands.
Note you may need to deploy and enter a python debugger pod on kubernetes to curl the address.
To read a samples data, we need to know the sol number, a 5 digit number indicating the day of the observation.
In our curl command we lew ```sol_key = 'sol<sol_number'```. Thus we read that sol with
```bash
$ curl <IP_ADDRESS>:<PORT>/read/<sol_key>
```
This returns a dictionary structure showing the perctage of each element within the sample. The output will look something like
```bash
{
  "Al2O3": "9.56", 
  "Br": "0.0032", 
  "CaO": "7.38", 
  "Cl": "0.61", 
  "Cr2O3": "0.42", 
  "FeO": "21", 
  "K2O": "0.59", 
  "MgO": "6.53", 
  "MnO": "0.44", 
  "Na2O": "2.22", 
  "Ni": "0.0311", 
  "P2O5": "0.53", 
  "SO3": "5.18", 
  "SiO2": "43.7", 
  "TiO2": "1.54", 
  "Zn": "0.0269"
}
```
with elements as keys and perctages as values to the dictionary.
We can now begin with creating. We can create a sample or sol using
```bash
$ curl -X GET <IP_ADDRESS>:<PORT>/create/<sol_key>
```
This will create an empty sol whose percentages are zero for every element. 
Since our element data is empty, we might now wish to define some percentages. The general formula is to 
```bash
$ curl -X POST <IP_ADDRESS>:<PORT>/update/<sol_key>/<element>/<value>
```
This will update the value associated with the element in the sol's dictionary.
To delete a sol, we similary run
```bash
$ curl -X POST <IP_ADDRESS>:<PORT>/delete/<sol_key>
```
If we now try to read the sol, we will get a "does not exist" message. the data is gone from teh database.

## JOB OPERATIONS 

Our application also offers the ability to complete jobs. The job we have described involves requesting a specific element,
and the application returns a histogram of the prectage abundancies of that element across all the smaples.
To requests such a job, we use
```bash
$ curl -X POST <IP_ADDRESS>:<PORT>/jobs/request/<element>
```
Notice we are returned a job id. This route submits a job request to the jobs queue, where a background worker script will handle the job.
We can keep updated with the status of our job with
```bash
$ curl <IP_ADDRESS>:<PORT>/jobs/status/<job_id>
```
The jobs typically finishes pretty quickly. When we find that our job is completed we can curl for the results.
Since the results are in the form of a histogram, we must specify a location for out image to be saved. 
The command thus looks something like:
```bash
$ curl -X POST <IP_ADDRESS>:<PORT>/jobs/results/<job_id> --output <destination>
```
This saved the image to our destination. You will find the typical histogram looks like this ![histogram](https://github.com/lukewilson37/coe332-MarsSoilSampleAnalysis/blob/main/test.png)





