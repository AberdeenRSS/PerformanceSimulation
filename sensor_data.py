import datetime
from pymongo import MongoClient
import pandas as pd
import matplotlib.pyplot as plt
 
# Provide the mongodb atlas url to connect python to mongodb using pymongo
CONNECTION_STRING = ""
ROCKET_NAME = 'Spatula'
FLIGHT_NAME = 'Flight 2023-05-04T15:09:27.413381'

# Create a connection using MongoClient. You can import MongoClient or use pymongo.MongoClient
client = MongoClient(CONNECTION_STRING)

# Create the database for our example (we will use the same database throughout the tutorial
db = client['rocketry']
  
vessel_collection = db['vessels']

vessel = vessel_collection.find({'name': {'$eq': ROCKET_NAME}})[0]

flight_collection = db['flights']

flight = flight_collection.find({'name': {'$eq': FLIGHT_NAME}, '_vessel_id': { '$eq': str(vessel['_id']) }})[0]

flight_data_collection = db['flight_data_compact']

def get_data_for_part(part_name: str, start: datetime.datetime, end: datetime.datetime):

    part = [ x for x in vessel['parts'] if x['name'] == part_name][0]

    measured = [x for x in flight['measured_parts'].items() if x[0] == part['_id']][0][1]

    data_names = [x['name'] for x in measured]

    raw = list(flight_data_collection.find({'metadata._flight_id': {'$eq': str(flight['_id'])}, 'metadata.part_id': {'$eq': part['_id'] }, '_start_time': { '$gte': start, '$lt': end } }))

    data_agg = {'Time': list[datetime.datetime]()}

    for name in data_names:
        data_agg[name] = list()

    for d in raw:
        for m in d['measurements']:
            data_agg['Time'].append(datetime.datetime.fromtimestamp(m[0]))
            i = 0
            for mm in m[1]:
                data_agg[data_names[i]].append(mm)
                i += 1

    return pd.DataFrame(data_agg)

flight_1_start = datetime.datetime.fromisoformat('2023-05-04T15:22:00.000+01:00')
flight_1_end = datetime.datetime.fromisoformat( '2023-05-04T15:22:25.000+01:00')

flight_2_start = datetime.datetime.fromisoformat('2023-05-04T15:22:48.000+01:00')
flight_2_end = datetime.datetime.fromisoformat( '2023-05-04T15:23:02.000+01:00')


dataframe = get_data_for_part('Gyroscope',flight_2_start, flight_2_end)
dataframe.plot(x='Time', y=['rotation-x', 'rotation-y', 'rotation-z'])

dataframe = get_data_for_part('Accelerometer', flight_2_start, flight_2_end)
dataframe.plot(x='Time', y=['acceleration-x', 'acceleration-y', 'acceleration-z'])

plt.show()


print('x')