#!/bin/bash


while getopts ":n:" opt; do
  case $opt in
    n) name="$OPTARG"
    ;;
    \?) echo "Invalid option -$OPTARG" >&2
    ;;
  esac
done

OW_OUT_DIR=/home/ow/shared
HOST_OUT_DIR=$PWD

xhost +

if [ -z "$name" ]
then # The name of the container is not set
    NAME="worm"
else # Name is set, use it
    NAME="$name"
fi
echo $NAME

sudo docker run -d \
--name $NAME \
--device=/dev/dri:/dev/dri \
--volume="$HOME/.Xauthority:/root/.Xauthority:rw" \
--env="DISPLAY" \
--net=host \
-e OW_OUT_DIR=$OW_OUT_DIR \
--privileged \
-v $HOST_OUT_DIR:$OW_OUT_DIR:rw \
-it \
openworm/openworm \

# Make a folder to move the data from the simulations
# sudo docker exec $NAME mkdir data
sudo docker cp ./into_container/run_c302.sh $NAME:home/ow/
sudo docker cp ./into_container/run_c302_nrn.sh $NAME:home/ow/
sudo docker exec $NAME mkdir data

