"""
https://www.instructables.com/Accessing-Your-Solaredge-Data-Using-Python/
https://www.solaredge.com/sites/default/files//se_monitoring_api.pdf

"""
import requests
import json
import os
import datetime
import pandas as pd
import matplotlib as plt

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


"""
start_date and end_date are in the format 'yyyy-mm-dd'
"""
def get_data(start_date=None, end_date=None):

    sites = issue_request('https://monitoringapi.solaredge.com/sites/list?api_key=%s' % API_KEY)
    overview = issue_request('https://monitoringapi.solaredge.com/site/%s/overview?api_key=%s' % (SITE_ID, API_KEY))
    details = issue_request('https://monitoringapi.solaredge.com/site/%s/details?api_key=%s' % (SITE_ID, API_KEY))
    data_period = issue_request('https://monitoringapi.solaredge.com/site/%s/dataPeriod?api_key=%s' % (SITE_ID, API_KEY))
    if start_date is None:
        start_date = data_period['dataPeriod']['startDate']
    y, m, d = get_ymd(start_date)
    start_date = datetime.datetime(y, m, d)
    if end_date is None:
        end_date = data_period['dataPeriod']['endDate']
    y, m, d = get_ymd(end_date)
    end_date = datetime.datetime(y, m, d)
    done = False
    energy_details = {}
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
            if meter['type'] not in energy_details.keys():
                energy_details[meter['type']] = meter['values']
            else:
                energy_details[meter['type']] = energy_details[meter['type']] + meter['values'][1:len(meter['values'])]

        if not done:
            start_date = one_year_out
    joined_energy_details = []
    for i in range(0, len(energy_details['FeedIn'])):
        feedIn = energy_details['FeedIn'][i].get('value', 0.0)
        production = energy_details['Production'][i].get('value', 0.0)
        consumption = energy_details['Consumption'][i].get('value', 0.0)
        self_consumption = energy_details['SelfConsumption'][i].get('value', 0.0)
        purchased = energy_details['Purchased'][i].get('value', 0.0)

        if i == len(energy_details['FeedIn']) - 1:
            if feedIn + production + consumption + self_consumption + purchased > 0.0:
                joined_entry = {
                    'date': energy_details['FeedIn'][i]['date'],
                    'FeedIn': feedIn/1000,
                    'Production': production/1000,
                    'Consumption': consumption/1000,
                    'SelfConsumption': self_consumption/1000,
                    'Purchased': purchased/1000
                }
                joined_energy_details.append(joined_entry)
    return energy_details, joined_energy_details

if __name__ == '__main__':
    data, joined_data = get_data()
    print(json.dumps(data, indent=4))
    print(json.dumps(joined_data, indent=4))