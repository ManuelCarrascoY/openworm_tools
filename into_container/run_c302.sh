#!/bin/bash

# RUN a python script inside c302 (USING THE JAVA PYNML)
# Check you have all the folder 

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
echo ${NAME}


if [ -z "$parameters" ]
then # The parameters set are not set
    PARAMS="A"
else # Parameters are set
    PARAMS="$parameters"
fi
echo $PARAMS

# RUN THE SCRIPT IN C302

cd c302
sudo python setup.py install
python c302/c302_${NAME}.py $PARAMS
pynml examples/LEMS_c302_${PARAMS}_${NAME}.xml

# Move the data into the data folder for exporting from container
mkdir ../data/c302_${PARAMS}_${NAME}
cp c302_${PARAMS}_${NAME}.dat \
c302_${PARAMS}_${NAME}.activity.dat \
c302_${PARAMS}_${NAME}.muscles.dat \
c302_${PARAMS}_${NAME}.muscles.activity.dat \
-t ../data/c302_${PARAMS}_${NAME}

cp examples/LEMS_c302_${PARAMS}_${NAME}.xml \
examples/c302_${PARAMS}_${NAME}.net.nml \
-t ../data/c302_${PARAMS}_${NAME}

