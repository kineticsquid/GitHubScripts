#!/bin/bash

ic target -r us-south
ic target -g default
ic fn namespace target utils

ic fn action update log log.py --kind python:3 --web true -p GMAIL_ID ${GMAIL_ID} -p GMAIL_PW ${GMAIL_PW} -p EMAIL_SSL_PORT ${EMAIL_SSL_PORT}

# Get the definition of the function
ic fn action get log

# invoke the function
curl --request POST --url 'https://us-south.functions.appdomain.cloud/api/v1/web/22eb44de-1265-44ac-9de7-076b9f5f58a4/default/log.json' --header 'accept: application/json' --header 'Content-Type: application/json' --data '{"TITLE": "Log Test", "COMMANDS": ["date", "printenv"], "TARGET_EMAIL": "'${TARGET_EMAIL}'"}'

# invoke the function
curl --request POST --url 'https://us-south.functions.appdomain.cloud/api/v1/web/22eb44de-1265-44ac-9de7-076b9f5f58a4/default/log.json' --header 'accept: application/json' --header 'Content-Type: application/json' --data '{"TITLE": "Log Test", "TEXT": "This is a test.", "TARGET_EMAIL": "'${TARGET_EMAIL}'"}'

# See the log results
echo "Make sure the activation reported by the next command is the most recent one executed. Look for activation id"
ic fn activation get -l

echo "https://us-south.functions.appdomain.cloud/api/v1/web/22eb44de-1265-44ac-9de7-076b9f5f58a4/default/log"

