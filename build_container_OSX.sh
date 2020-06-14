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
HOST_OUT_DIR=$PWD/shared

xhost +

if [ -z "$name" ]
then # The name of the container is not set
    NAME="worm"
else # Name is set, use it
    NAME="$name"
fi
echo $NAME

docker run -d \
--name $NAME \
--device=/dev/dri:/dev/dri \
--volume="$HOME/.Xauthority:/root/.Xauthority:rw" \
-e DISPLAY=192.168.1.48:0 \
--net=host \
-e OW_OUT_DIR=$OW_OUT_DIR \
--privileged \
-v $HOST_OUT_DIR:$OW_OUT_DIR:rw \
-it \
openworm/openworm \

docker exec $NAME cp ./shared/modified_scripts/* -t /home/ow/c302/c302/
docker exec $NAME cp ./shared/modified_data/* -t /home/ow/c302/c302/data/
docker exec $NAME sudo python /home/ow/c302/setup.py install

docker exec $NAME sudo apt-get -y update
docker exec $NAME sudo apt-get -y install graphviz
docker exec $NAME sudo pip install graphviz
docker exec $NAME sudo apt-get -y install feh

# Make a folder to move the data from the simulations
# sudo docker exec $NAME mkdir data
# sudo docker cp ./into_container/run_c302.sh $NAME:home/ow/
# sudo docker cp ./into_container/run_c302_nrn.sh $NAME:home/ow/
# sudo docker exec $NAME mkdir data

