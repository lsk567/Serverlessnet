#!/bin/bash

# echo output
# set -x
# set -v

# run the container
docker run --name containernet -it --rm --privileged --pid='host' \
	-v /var/run/docker.sock:/var/run/docker.sock \
	-v "$(pwd)":/containernet/lambda  \
	containernet/containernet /bin/bash

