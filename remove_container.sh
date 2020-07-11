#!/bin/bash

# This shell script deletes an open container. 
# It takes a flag '-n NAME' as the name of the containter, by default, the name is set to 'worm'

while getopts ":n:" opt; do
  case $opt in
    n) name="$OPTARG"
    ;;
    \?) echo "Invalid option -$OPTARG" >&2
    ;;
  esac
done


xhost +

if [ -z "$name" ]
then # The name of the container is not set
    NAME="worm"
else # Name is set, use it
    NAME="$name"
fi

docker stop $NAME
docker rm $NAME
