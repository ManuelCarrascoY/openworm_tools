#!/bin/bash

# RUN a python script inside c302 (USING NEURON)
# Check you have all the folders
ls

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

# RUN THE SCRIPT IN C302

cd c302
#sudo python setup.py install
python c302/c302_${NAME}.py $PARAMS

# Try with Neuron
cd examples
pynml LEMS_c302_${PARAMS}_${NAME}.xml -neuron
nrnivmodl
nrngui LEMS_c302_${PARAMS}_${NAME}_nrn.py
#pynml c302_${PARAMS}_${NAME}.net.nml -graph 2c 

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

