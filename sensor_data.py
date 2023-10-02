import requests
import json

BASE_URL = 'http://rocketry.sidneypauly.me:5000'
VESSEL_NAME = 'Spatula (Production)'
PART_NAME = 'Battery'
FLIGHT_NAME = 'flight_1'


vessels_request = requests.get(f'{BASE_URL}/vessel/get_by_name/{VESSEL_NAME}')
vessels = vessels_request.json()
vessel = vessels[0]

battery_part = [p for p in vessel["parts"] if (PART_NAME in p["name"])][0]

flights_request = requests.get(f'{BASE_URL}/flight/get_by_name/{vessel["_id"]}/{FLIGHT_NAME}')
flights = flights_request.json()
flight = flights[0]

measurements_request = requests.get(f'{BASE_URL}/flight_data/get_range/{flight["_id"]}/{battery_part["_id"]}/{flight["start"]}/{flight["end"]}')
measurements = measurements_request.json()
