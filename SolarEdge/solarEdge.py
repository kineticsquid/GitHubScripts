"""
https://www.instructables.com/Accessing-Your-Solaredge-Data-Using-Python/
https://www.solaredge.com/sites/default/files//se_monitoring_api.pdf

"""
import requests
import json
import os
import datetime

API_KEY = os.environ['API_KEY']
SITE_ID = os.environ['SITE_ID']

def issue_request(url):
    response = requests.get(url)
    if response.status_code != 200:
        raise Exception(response.content)
    results = response.json()
    return results

def get_ymd(date_string):
    return int(date_string[0:4]), int(date_string[5:7]), int(date_string[8:10])


def get_data():

    sites = issue_request('https://monitoringapi.solaredge.com/sites/list?api_key=%s' % API_KEY)
    overview = issue_request('https://monitoringapi.solaredge.com/site/%s/overview?api_key=%s' % (SITE_ID, API_KEY))
    details = issue_request('https://monitoringapi.solaredge.com/site/%s/details?api_key=%s' % (SITE_ID, API_KEY))
    data_period = issue_request('https://monitoringapi.solaredge.com/site/%s/dataPeriod?api_key=%s' % (SITE_ID, API_KEY))
    start_date_str = data_period['dataPeriod']['startDate']
    y, m, d = get_ymd(start_date_str)
    start_date = datetime.datetime(y, m, d)
    end_date_str = data_period['dataPeriod']['endDate']
    y, m, d = get_ymd(end_date_str)
    end_date = datetime.datetime(y, m, d)
    done = False
    energyDetails = {}
    while not done:
        one_year_out = datetime.datetime(start_date.year + 1, start_date.month, start_date.day)
        delta = end_date - one_year_out
        if delta.days > 0:
            start = str(start_date)
            end = str(one_year_out)
        else:
            start = str(start_date)
            end = str(end_date)
            done = True
        energy_detail_url = 'https://monitoringapi.solaredge.com/site/%s/energyDetails' % SITE_ID
        energy_detail_url += '?timeUnit=DAY&startTime=%s&endTime=%s&api_key=%s' % (start, end, API_KEY)
        detail = issue_request(energy_detail_url)
        for meter in detail['energyDetails']['meters']:
            if meter['type'] not in energyDetails.keys():
                energyDetails[meter['type']] = meter['values']
            else:
                energyDetails[meter['type']] = energyDetails[meter['type']] + meter['values'][1:len(meter['values'])]

        if not done:
            start_date = one_year_out
    return energyDetails

if __name__ == '__main__':
    data = get_data()
    print(json.dumps(data, indent=4))