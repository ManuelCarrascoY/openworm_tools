#!/bin/bash

cd ~

# INSTALL OPENWORM DOCKER

sudo docker openworm/openworm
# Check the Available Images 
sudo docker images
# there should be 3 images: ubuntu, openworm 0.9 and openworm latest

cd - 
