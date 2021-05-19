#!/bin/bash

ibmcloud target -r us-south
ibmcloud target -g default
ibmcloud fn namespace target utils

ibmcloud fn action update hw hw.py --kind python:3 --web true -p GILLIGAN USS_MINNOW

# Get the definition of the function
ibmcloud fn action get hw
# invoke the function
ibmcloud fn action invoke hw --blocking  -p ELEPHANT CLYDE
# See the log results
echo "Make sure the activation reported by the next command is the most recent one executed. Look for activation id"
ibmcloud fn activation get -l

echo "https://us-south.functions.appdomain.cloud/api/v1/web/22eb44de-1265-44ac-9de7-076b9f5f58a4/default/hw"

