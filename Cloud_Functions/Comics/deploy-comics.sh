#!/bin/bash

ic target -r us-south
ic target -g default
ic fn namespace target utils

ic fn action update Comics ./comics.py --kind python:3.7 -p GMAIL_ID ${GMAIL_ID} -p GMAIL_PW ${GMAIL_PW} -p TARGET_EMAIL ${TARGET_EMAIL} --web true --memory 512 --timeout 240000

# Get the definition of the function
ic fn action get Comics

# invoke the function
#
# Also, gmail password works locally but does not work from cloud function, one needs an app
# password: https://support.google.com/accounts/answer/185833

ic fn action invoke Comics --blocking
#ibmcloud fn action invoke Comics --blocking  -p GMAIL_ID ${GMAIL_ID} -p GMAIL_PW ${GMAIL_PW} -p TARGET_EMAIL ${TARGET_EMAIL}

# See the log results
echo "Make sure the activation reported by the next command is the most recent one executed. Look for activation id"
echo "ibmcloud fn activation get -l"

