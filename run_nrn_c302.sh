#!/bin/bash

# Shell script to run a neuronal simulation using NEURON
# Takes the 'c302/c302_reference.py' in host and executes it within the docker container. 
# Has 3 flags: '-n NameOfContainer', '-r NameOfReference' and 'p Parameters'. 
# By default, if nothing is stated, NameOfContainer = 'worm', NameOfReference = 'IClamp' and Parameters = 'A'


while getopts ":n:r:p:" opt; do
  case $opt in
    n) cont_name="$OPTARG" #	Name of the docker container
    ;;
    r) reference="$OPTARG" #	Reference of the python script (e.g. IClamp)
    ;;
    p) parameters="$OPTARG" #	Parameters to use in the simulation
    ;;
    \?) echo "Invalid option -$OPTARG" >&2
    ;;
  esac
done

xhost +

if [ -z "$cont_name" ]
then # The name of the conteiner is not set
    NAME="worm"
else # Container name is set, use it
    NAME="$cont_name"
fi


if [ -z "$reference" ]
then # The reference is not set
    REF="IClamp"
else # Reference is set, use it
    REF="$reference"
fi
echo $REF

if [ -z "$parameters" ]
then # The parameters are not set
    PARAMS="A"
else # Parameters are set, use them
    PARAMS="$parameters"
fi

FILENAME="c302_${REF}.py"

docker start $NAME
docker cp c302/$FILENAME $NAME:home/ow/c302/c302/ #Copy the python script from host to container
docker exec $NAME ./shared/run_c302_nrn.sh -r ${REF} -p ${PARAMS} #Executes the 'shared/run_c302_nrn.sh in the container'
mv shared/data/* c302/simulation_data/ #Moves the resulting data into the host

