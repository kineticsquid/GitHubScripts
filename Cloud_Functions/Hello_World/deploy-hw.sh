#!/bin/bash

ibmcloud target -r us-east
ibmcloud target -g "JKs Resource Group"
ibmcloud fn namespace target Kellerman-Functions

# First time through need to create the package with
#
# ibmcloud fn package create utils --shared yes
#
# and create the function (as opposed to updating it):
#
# ibmcloud fn action create hw hw.py --kind python:3 --web true -p FOO BAR

# Update utils package and environment function
#ibmcloud fn package update utils --shared yes
ibmcloud fn action update utils/hw hw.py --kind python:3 --web true -p FOO BAR

# Now list the package
ibmcloud fn package get utils
# Get the definition of the function
ibmcloud fn action get utils/hw
# invoke the function
ibmcloud fn action invoke utils/hw --blocking  -p ELEPHANT CLYDE
# See the log results
echo "Make sure the activation reported by the next command is the most recent one executed. Look for activation id"
ibmcloud fn activation get -l

echo "URL is https://us-east.functions.appdomain.cloud/api/v1/web/634e7a7f-9928-4744-8190-f4bf5d671142/utils/hw"

