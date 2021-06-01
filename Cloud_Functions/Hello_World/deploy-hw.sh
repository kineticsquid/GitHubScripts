#!/bin/bash

ic target -r us-south
ic target -g default
ic fn namespace target utils

ic fn action update hw hw.py --kind python:3 --web true -p GILLIGAN USS_MINNOW

# Get the definition of the function
ic fn action get hw
# invoke the function
ic fn action invoke hw --blocking  -p ELEPHANT CLYDE
# See the log results
echo "Make sure the activation reported by the next command is the most recent one executed. Look for activation id"
ic fn activation get -l

echo "https://us-south.functions.appdomain.cloud/api/v1/web/22eb44de-1265-44ac-9de7-076b9f5f58a4/default/hw"

