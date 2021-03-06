#!/usr/bin/python

# The usual preamble
import numpy as np
import pandas as pd
import time

# Get data (NYC 311 service request dataset) and start cleanup
data = pd.read_csv('data/us_cities_states_counties.csv', delimiter='|')
data.dropna(inplace=True)
print "Done reading input file..."

start = time.time()

# Get all city information with total population greater than 500,000
data_big_cities = data[data["Total population"] > 500000]

# Compute "crime index" proportional to
# (Total population + 2*(Total adult population) - 2000*(Number of robberies)) / 100000
data_big_cities_stats = data_big_cities[
    ["Total population", "Total adult population", "Number of robberies"]].values
predictions = np.dot(data_big_cities_stats, np.array(
    [1.0, 2.0, -2000.0])) / 100000.0
data_big_cities["Crime index"] = predictions

# Aggregate "crime index" scores by state
data_big_cities["Crime index"][data_big_cities["Crime index"] >= 0.02] = 0.032
data_big_cities["Crime index"][data_big_cities["Crime index"] < 0.01] = 0.005
print data_big_cities["Crime index"].sum()
end = time.time()

print "Total end-to-end time: %.2f" % (end - start)
