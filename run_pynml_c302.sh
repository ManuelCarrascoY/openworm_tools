#!/bin/bash

while getopts ":n:r:p:" opt; do
  case $opt in
    n) cont_name="$OPTARG" #	Name of the docker container
    ;;
    r) reference="$OPTARG" #	Reference of the python script (i.e. IClamp)
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
docker cp c302/$FILENAME $NAME:home/ow/c302/c302/
docker exec $NAME ./shared/run_c302.sh -r ${REF} -p ${PARAMS}
mv shared/data/* c302/simulation_data/
