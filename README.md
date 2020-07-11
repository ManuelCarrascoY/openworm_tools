# Tools for the use of OpenWorm

In this repository you will find:
* Shell scripts developed for using the OpenWorm framework under a docker container.
* Jupyter Notebooks developed in Python 3 for interpreting the data. 
* The files developed for the forward and backward locomotion model in *Caenorhabditis elegans*. 

(The repository has been developed as part of my Bachelor Thesis Project: **Models of Neuromorphic Computing: Brain-body-environment simulation of Caenorhabditis elegans forward and backward locomotion**)

---

The results of the forward and backward locomotion model are the following: 

![Forward locomotion](/images/FW_gif.gif)


![Backward locomotion](/images/BW_gif.gif)

This codes are used to edit the c302_reference.py scripts and run them inside a docker container by following some easy steps. 
**1. Use c302 inside the container and represent the neuron and muscle activity**
**2. Run a complete simulation using c302 and Sibernetic**

## About OpenWorm

[OpenWorm](http://www.openworm.org) aims to build the first comprehensive computational model of Caenorhabditis elegans (C. elegans), a microscopic roundworm. With only a thousand cells, it solves basic problems such as feeding, mate-finding and predator avoidance. Despite being extremely well-studied in biology, a deep, principled understanding of the biology of this organism remains elusive.

## About Docker Containers

A [Docker](https://www.docker.com/get-started) container is a self-contained environment in which you can run OpenWorm simulations. It's fully set up to get you started by following the steps above. At the moment, it runs simulations and produces visualizations for you, but these visualizations must be viewed outside of the Docker container. 

### What does the OpenWorm docker contain? 

Inside the container, we can find all the necessary tools to make the simulation of the nematode C. Elegans using c302, pyNeuroML, NEURON, pyOpenWorm and Sibernetic. 

## Quick Start

### Install Docker

If you are a ubuntu user, you only need to run the following: 

    git clone https://github.com/ManuelCarrascoY/openworm_tools.git
    cd openworm_tools/
    ./install_docker.sh

This will install docker and login into you docker account. For Mac or Window users, make sure to follow the instructuions to install docker in your system from the [Docker website](https://www.docker.com/get-started)

### Install Openworm

Clone the Openworm repository and the Openworm docker image by executing the following: 

    ./install_openworm.sh

### Use the Docker Container

A container can be built with: 

    ./build_container.sh -n ContainerName #Set a name for the container

Once the Container is build, if you want to close and erase it (not this will delete all work done on that container)

    ./remove_container.sh -n ContainerName

If you want to use the container and explore what is inside, you can attach to it:

    ./attach_to_container.sh -n ContainerName

**Mac Users**: 

In order to open GUI applications fron the docker container, follow these steps (you will need homebrew installed)
1. Install XQuartz

    brew cask install XQuartz

2. Install Socat

    brew install socat

3. Run socat (Check this [tutorial](https://www.youtube.com/watch?v=PKyj8sbZNYw))

    socat TCP-LISTEN:6000,reuseaddr,fork UNIX-CLIENT:\"$DISPLAY\"

4. Find the IP of your system (should appeart under 'inet 192.168...') 

    ifconfig en0

5. Change in *build_container_OSX.sh* the DISPLAY IP

## 1. Use c302 to represent neuron and muscle activity

Create your own network by modifying the *c302/c302_tutorial.py* file (WorkInProgress). Note that this script has to be done in python2, the openworm framework that still has issues when using python3. 

Run a simulation with the *c302/c302_IClamp.py*:
**Using pyNeuroMl**

    ./run_pynml_c302.sh -n ContainerName -r Reference -p Parameters #Reference = IClamp, Parameters = A

**Using NEURON**

    ./run_nrn_c302.sh -n ContainerName -r Reference -p Parameters #Reference = IClamp, Parameters = A

The resulting data files are stored in *c302/data/*

### Reading the data in a Jupyter Notebook 

(WorkInProgress)

## 2. Use c302 and Sibernetic together

(WorkInProgress)
