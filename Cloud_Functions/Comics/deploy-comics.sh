#!/bin/bash

ibmcloud target -r us-east
ibmcloud target -g "JKs Resource Group"
ibmcloud fn namespace target Kellerman-Functions

ibmcloud fn action update utils/Comics ./comics.py --kind python:3.7

#ibmcloud fn trigger update "Comics Daily" -p GMAIL_ID ${GMAIL_ID} -p GMAIL_PW ${GMAIL_PW} -p TARGET_EMAIL ${TARGET_EMAIL} --param cron "40 * * * *"
#
#ibmcloud fn rule update comics_rule "Comics Daily" utils/Comics

# Get the definition of the function
ibmcloud fn action get utils/Comics

# Get the definition of the trigger
#ibmcloud fn trigger get "Comics Daily"

# Get the definition of the rule
#ibmcloud fn rule get comics_rule

# invoke the function
#
# Note, when setting COMICS value as an environment variable at least in lanuch configs in Pycharm,
# do not leave spaces. e.g. do this "[\"frazz\",\"getfuzzy\"]"
#
# Also, gmail password works locally but does not work from cloud function, one needs an app
# password: https://support.google.com/accounts/answer/185833

ibmcloud fn action invoke utils/Comics --blocking  -p GMAIL_ID ${GMAIL_ID} -p GMAIL_PW ${GMAIL_PW} -p TARGET_EMAIL ${TARGET_EMAIL}

# See the log results
echo "Make sure the activation reported by the next command is the most recent one executed. Look for activation id"
echo "ibmcloud fn activation get -l"

