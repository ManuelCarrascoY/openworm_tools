#!/bin/bash

# Creates a container using the openworm image
# Adds specification to have a /shared folder between the host and the container
# Also provides the container with the information to run GUI apps in your host display
# It takes a flag '-n NAME' as the name of the containter, by default, the name is set to 'worm'

# Set the '-n NAME' tag
while getopts ":n:" opt; do
  case $opt in
    n) name="$OPTARG"
    ;;
    \?) echo "Invalid option -$OPTARG" >&2
    ;;
  esac
done

OW_OUT_DIR=/home/ow/shared
HOST_OUT_DIR=$PWD/shared

xhost + #Enable display into your host

if [ -z "$name" ]
then # The name of the container is not set, use 'worm'
    NAME="worm"
else # Name is set, use it
    NAME="$name"
fi
echo $NAME

# Create the container with all the specifications
docker run -d \
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


docker exec $NAME cp ./shared/modified_scripts/* -t /home/ow/c302/c302/ #Copy modified_scripts to c302/
docker exec $NAME cp ./shared/modified_data/* -t /home/ow/c302/c302/data/ #Copy modified_data to c302/data/
docker exec $NAME sudo python /home/ow/c302/setup.py install

docker exec $NAME sudo apt-get -y update
docker exec $NAME sudo apt-get -y install graphviz
docker exec $NAME sudo pip install graphviz #Install graphviz
docker exec $NAME sudo apt-get -y install feh #Install feh to open images


