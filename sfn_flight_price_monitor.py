# Chck lowest flight price from google QPX API
# Zheng Liu, version 1.0 on 2016-08-04


import urllib2
import json
import re
import datetime
from threading import Timer
import sched, time

with open('GoogleAPIkey.txt') as key_file:
    key = key_file.read()
url = "https://www.googleapis.com/qpxExpress/v1/trips/search?key=" + key
# Load key file and generate url

code = {
  "request": {
    "slice": [
      {
        "origin": "ROC",
        "destination": "SAN",
        "date": "2016-11-10",
        "permittedDepartureTime": {
          "latestTime": "06:30"
        },
        "permittedCarrier": [
          "UA"
        ]
      },
      {
        "origin": "SAN",
        "destination": "ROC",
        "date": "2016-11-16",
        "permittedDepartureTime": {
          "earliestTime": "22:00"
        },
        "permittedCarrier": [
          "UA"
        ]
      }
    ],
    "passengers": {
      "adultCount": 1,
      "infantInLapCount": 0,
      "infantInSeatCount": 0,
      "childCount": 0,
      "seniorCount": 0
    },
    "solutions": 1,
    "refundable": 'false'
  }
}

# Thursday back code
code_thu = {
  "request": {
    "slice": [
      {
        "origin": "ROC",
        "destination": "SAN",
        "date": "2016-11-10",
        "permittedDepartureTime": {
          "latestTime": "06:59"
        },
        "permittedCarrier": [
          "UA"
        ]
      },
      {
        "origin": "SAN",
        "destination": "ROC",
        "date": "2016-11-17",
        "permittedDepartureTime": {
          "earliestTime": "08:00",
          "latestTime": "12:00"
        },
        "permittedCarrier": [
          "UA"
        ]
      }
    ],
    "passengers": {
      "adultCount": 1,
      "infantInLapCount": 0,
      "infantInSeatCount": 0,
      "childCount": 0,
      "seniorCount": 0
    },
    "solutions": 5,
    "refundable": 'false'
  }
}

s = sched.scheduler(time.time, time.sleep)

def get_min_price(sc):
# Return on Wednesday
    # Get API response
    jsonreq = json.dumps(code, encoding = 'utf-8')
    req = urllib2.Request(url, jsonreq, {'Content-Type': 'application/json'})
    flight = urllib2.urlopen(req)
    response = flight.read()
    flight.close()

    # Get current time
    current_time = str(datetime.datetime.utcnow()) # Use UTC time

    # Write original JSON into file
    file_name = 'sfn fly back Wed ', current_time, '.txt' # this is a tup type
    file_name_str = ''.join(file_name) # Convert to str
    with open(file_name_str, 'w') as outfile:
        json.dump(response, outfile)

    # Extract lowest price and Storage
    js_response = json.loads(response)
    min_price_unicode = js_response['trips']['tripOption'][0]['pricing'][0]['saleTotal']
    min_price = re.findall(r'\d+', min_price_unicode)[0] # Use regular expresion to extract number from unicode

    print min_price + ', at time: ' + current_time

    with open("sfnWed.txt", "a") as myfile:
        myfile.write(min_price + ', at time: ' + current_time)
        myfile.write('\n') # Line change in saved file


# Return on Thursday
    # Get API response
    jsonreq = json.dumps(code_thu, encoding = 'utf-8')
    req = urllib2.Request(url, jsonreq, {'Content-Type': 'application/json'})
    flight = urllib2.urlopen(req)
    response = flight.read()
    flight.close()

    # Write original JSON into file
    file_name = 'sfn fly back Thu ', current_time, '.txt' # this is a tup type
    file_name_str = ''.join(file_name) # Convert to str
    with open(file_name_str, 'w') as outfile:
        json.dump(response, outfile)

    # Extract lowest price and Storage
    js_response = json.loads(response)
    min_price_unicode = js_response['trips']['tripOption'][0]['pricing'][0]['saleTotal']
    min_price = re.findall(r'\d+', min_price_unicode)[0] # Use regular expresion to extract number from unicode

    print min_price + ', at time: ' + current_time

    with open("sfnThu.txt", "a") as myfile:
        myfile.write(min_price + ', at time: ' + current_time)
        myfile.write('\n') # Line change in saved file

    # Loop every hour
    # sc.enter(3600, 1, get_min_price, (sc,))

s.enter(0, 1, get_min_price, (s,))
s.run()
