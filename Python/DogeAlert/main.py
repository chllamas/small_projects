#This example uses Python 2.7 and the python-request library.

import os
import time
from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import json

update_in_minutes = 5

def update_JSON_data():
    url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'
    parameters = {
      'start':'6',
      'limit':'1',
      'convert':'USD'
    }
    headers = {
      'Accepts': 'application/json',
      'X-CMC_PRO_API_KEY': '07591b6a-1876-4a87-85c7-85db6343b48e',
    }

    session = Session()
    session.headers.update(headers)

    try:
      response = session.get(url, params=parameters)
      data = json.loads(response.text)
      outfile = open('output.json', 'w')
      json.dump(data, outfile)
      outfile.close()
    except (ConnectionError, Timeout, TooManyRedirects) as e:
      print(e)

last_modified_time_since_epoch = os.path.getmtime('output.json')
time_since_epoch = time.time()

if (time_since_epoch - last_modified_time_since_epoch) > (update_in_minutes*60):
  print ("Updating JSON")
  update_JSON_data()

with open("output.json", "r") as read_file:
  data = json.load(read_file)

print(data['data'][0]['quote']['USD']['price'])