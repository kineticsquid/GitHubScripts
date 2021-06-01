import requests
import os
import json

if __name__ == '__main__':
    ID = os.environ['ID']
    PW = os.environ['PW']
    url = 'https://us-south.functions.appdomain.cloud/api/v1/web/22eb44de-1265-44ac-9de7-076b9f5f58a4/default/log.json'
    commands = ['ibmcloud login -a cloud.ibm.com -u %s -p %s -g default -r us-south' % (ID, PW)]
    headers = {'Content-Type': 'application/json',
               'accept': 'application/json'}
    data = {'TITLE': 'Log CF Request Test',
            'TARGET_EMAIL': ID,
            'COMMANDS': commands}

    response = requests.post(url, headers=headers, data=json.dumps(data))
    print(response.status_code)
    print(response.content)

