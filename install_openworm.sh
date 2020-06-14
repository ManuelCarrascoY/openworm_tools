#!/bin/bash

cd ~

# INSTALL OPENWORM DOCKER

docker pull openworm/openworm
# Check the Available Images 
docker images
# there should be 3 images: ubuntu, openworm 0.9 and openworm latest

cd - 
