#!/bin/bash

ibmcloud target -r us-south
ibmcloud target -g default
ibmcloud fn namespace target utils

ibmcloud fn action invoke Comics --blocking

# See the log results
echo "Make sure the activation reported by the next command is the most recent one executed. Look for activation id"
echo "ibmcloud fn activation get -l"

