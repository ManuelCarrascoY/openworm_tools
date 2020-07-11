# Tools for the use of OpenWorm

The repository has been developed as part of my Bachelor Thesis Project: **Models of Neuromorphic Computing: Brain-body-environment simulation of *Caenorhabditis elegans* forward and backward locomotion**

<div class="row">
  <div class="column">
    <img src=./images/real_nematode.png width="250">
  </div>
  <div class="column">
    <img src=./images/Logo_UC3M.png width="100">
  </div>
  <div class="column">
    <img src=./images/OW.jpeg width="100">
  </div>
</div>

In this repository you will find:
* Shell scripts developed for using the OpenWorm framework under a docker container.
* Jupyter Notebooks in Python 3 for interpreting the data. 
* Files for the forward and backward locomotion model in *Caenorhabditis elegans*. 

---

Results of the forward and backward locomotion model: 

![Forward locomotion](/images/FW_gif.gif)


![Backward locomotion](/images/BW_gif.gif)

---

# INTRODUCTION

## About OpenWorm 

[OpenWorm](http://www.openworm.org) aims to build the first comprehensive computational model of *Caenorhabditis elegans*: a microscopic roundworm nematode. Their approach towards building the nematode is to collect all the data from biological experiments and integrate it using software models. It has been divided into smaller software sub-projects that can be interconnected to provide various utilities inside the framework. For this project, I have made use of the c302 and Sibernetic frameworks. 

![OpenWorm](/images/)

![OpenWorm projects](/images/OW.png)

## About Docker Containers

A [Docker container](https://www.docker.com/get-started) is an isolated working place in which specific images can be run like the OpenWorm simulations. They allow to store code and all its dependencies so that applications are executed in a fast and secure way within different computers and operative systems. These containers can be executed from your terminal after installing Docker, and can run graphical user interface applications if executed with the proper display commands. The OpenWorm docker image contains all the necessary tools to make the simulation of the nematode C. Elegans using c302, pyNeuroML, NEURON, pyOpenWorm and Sibernetic (For more information, see the [OpenWorm repository](http://www.openworm.org))

![Docker container](/images/docker.png)

---
# Quick Start: Using OpenWorm

### Install Docker

If you are a ubuntu user, you only need to run the following commands within your terminal:

    git clone https://github.com/ManuelCarrascoY/openworm_tools.git
    cd openworm_tools/
    ./install_docker.sh

This will install docker and login into you docker account. For Mac or Window users, make sure to follow the instructuions to install docker in your system found in the [Docker website](https://www.docker.com/get-started).

### Use the Docker Container

A container can be built with the shell script `build_container.sh`

    ./build_container.sh -n ContainerName #Set a name for the container

If no name tag is added, the default name will be set to *worm*. 
(Also note that the first time you run this command, Docker will install the *openworm/latest* docker image and it may take a few minutes). 

Once the container is built, you can check its status with the following command: 

    docker ps -a 

Okay, now we have the container created, we can attach to it using: 

    ./attach_to_container.sh -n ContainerName

Once within, run an `ls` command and make sure you can find the PyOpenWorn, c302, neuron, sibernetic, pyNeuroML, master_openworm.py and shared directories.
To close the container type ´exit´, to escape the container use: *Ctrl+P* and *Ctrl+Q*. 

Once the Container is build, if you want to close and erase it (note this will delete any work done inside that container):

    ./remove_container.sh -n ContainerName


**Mac Users**: 

In order to open GUI applications fron the docker container, follow these steps (you will need homebrew installed)
1. Install XQuartz

    brew cask install XQuartz

2. Install Socat

    brew install socat

3. Run socat (Check this [tutorial](https://www.youtube.com/watch?v=PKyj8sbZNYw))

    socat TCP-LISTEN:6000,reuseaddr,fork UNIX-CLIENT:\"$DISPLAY\" &

5. Run the `build_container_OSX.sh` instead.

---

# Use c302 for Neuron and Muscle Activity

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
