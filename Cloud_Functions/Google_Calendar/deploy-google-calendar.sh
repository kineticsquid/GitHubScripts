#!/bin/bash

ibmcloud target -r us-east
ibmcloud target -g "JKs Resource Group"
ibmcloud fn namespace target Kellerman-Functions

virtualenv virtualenv
source virtualenv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt

cp google_calendar.py __main__.py
zip -r  virtualenv __main__.py credentials.json token.json
rm __main__.py

ibmcloud fn action update utils/google-calendar ./google-calendar.zip --kind python:3 --web true
 rm google-calendar.zip

# Now list the package
ibmcloud fn package get utils
# Get the definition of the function
ibmcloud fn action get utils/google-calendar
# invoke the function
ibmcloud fn action invoke utils/google-calendar --blocking  -p ELEPHANT CLYDE
# See the log results
echo "Make sure the activation reported by the next command is the most recent one executed. Look for activation id"
ibmcloud fn activation get -l

echo "URL is https://us-east.functions.appdomain.cloud/api/v1/web/634e7a7f-9928-4744-8190-f4bf5d671142/utils/google-calendar"
