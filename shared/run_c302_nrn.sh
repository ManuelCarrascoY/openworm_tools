#!/bin/bash

# Shell script to run a neuronal simulation using NEURON
# Takes the 'c302/c302_reference.py' in host and executes it within the docker container. 
# Has 2 flags: '-r NameOfReference' and 'p Parameters'. 
# By default, if nothing is stated, NameOfReference = 'IClamp' and Parameters = 'A'

ls #Check all of the folders of the container are there

while getopts ":r:p:" opt; do
  case $opt in
    r) reference="$OPTARG"
    ;;
    p) parameters="$OPTARG"
    ;;
    \?) echo "Invalid option -$OPTARG" >&2
    ;;
  esac
done

xhost +

if [ -z "$reference" ]
then # The referance name is not set
    NAME="IClamp"
else # Reference name is set, use it
    NAME="$reference"
fi

if [ -z "$parameters" ]
then # The parameters set are not set
    PARAMS="A"
else # Parameters are set
    PARAMS="$parameters"
fi

# RUN THE SCRIPT IN C302 FOR NEURON SIMULATION

cd c302
python c302/c302_${NAME}.py $PARAMS

cd examples
pynml LEMS_c302_${PARAMS}_${NAME}.xml -neuron # Generate the Neuron files
nrnivmodl # Compile the mod files (used for cell/ion channel definition)
nrngui LEMS_c302_${PARAMS}_${NAME}_nrn.py # Run the main Python for the simulation using Neuron
pynml c302_${PARAMS}_${NAME}.net.nml -graph 2c # Plot the connections of the simulation

# Move the generated files to the shared folder
mkdir ../../shared/data/c302_${PARAMS}_${NAME}_nrn
cp c302_${PARAMS}_${NAME}.dat \
c302_${PARAMS}_${NAME}.activity.dat \
c302_${PARAMS}_${NAME}.muscles.dat \
c302_${PARAMS}_${NAME}.muscles.activity.dat \
c302_${PARAMS}_${NAME}.gv.png \
-t ../../shared/data/c302_${PARAMS}_${NAME}_nrn
cp LEMS_c302_${PARAMS}_${NAME}.xml \
c302_${PARAMS}_${NAME}.net.nml \
-t ../../shared/data/c302_${PARAMS}_${NAME}_nrn


cd ../..
FILENAME="time.dat"
cp c302/examples/$FILENAME -t ./shared/data/c302_${PARAMS}_${NAME}_nrn

