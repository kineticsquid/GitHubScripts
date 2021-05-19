#!/bin/bash

ibmcloud target -r us-south
ibmcloud target -g default
ibmcloud fn namespace target utils

ibmcloud fn action update Comics ./comics.py --kind python:3.7 -p GMAIL_ID ${GMAIL_ID} -p GMAIL_PW ${GMAIL_PW} -p TARGET_EMAIL ${TARGET_EMAIL} --web true --memory 512 --timeout 240000

# These next two commands are done once and don't work for update
# ibmcloud fn trigger create Comics-daily --feed /whisk.system/alarms/alarm --param cron "0 7 * * *"
# ibmcloud fn rule create Comics-daily-rule Comics-daily Comics


# Get the definition of the function
ibmcloud fn action get Comics

# invoke the function
#
# Also, gmail password works locally but does not work from cloud function, one needs an app
# password: https://support.google.com/accounts/answer/185833

ibmcloud fn action invoke Comics --blocking
#ibmcloud fn action invoke Comics --blocking  -p GMAIL_ID ${GMAIL_ID} -p GMAIL_PW ${GMAIL_PW} -p TARGET_EMAIL ${TARGET_EMAIL}

# See the log results
echo "Make sure the activation reported by the next command is the most recent one executed. Look for activation id"
echo "ibmcloud fn activation get -l"

