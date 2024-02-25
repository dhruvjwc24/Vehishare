import googlemaps
from datetime import datetime
from geopy.geocoders import Nominatim
import matplotlib.pyplot as plt
import numpy as np
import csv as c
import math
from heapq import heapify, heappop, heappush

def main():
  gmaps_client = googlemaps.Client(key = "AIzaSyDU-q9Y3uZEOFY6Oo3H-NkViejWbrB59i8")

  ADDRESSES = {}

  data = {}

  wd = open('website_data.csv', 'r')
  cr = c.reader(wd)

  for index, row in enumerate(cr):
    if index == 0:
      for header in row:
        data[header] = []
    else:
      data['user'].append(row[0])
      data['source'].append(row[1])
      data['destination'].append(row[2])
      data['isDriver'].append(row[3])
      data['numSeats'].append(row[4])

  wd.close()

  drivers = []

  non_drivers = []

  print(data)

  for entry in range(len(data['user'])):
    user = data['user'][entry]
    # print(user)
    # print(user)
    geolocator = Nominatim(user_agent = "dhruvjwc@gmail.com")
    # print(geolocator)
    location = geolocator.geocode(data['destination'][entry])
    continue
    # print(location)

    lat_long = (location.latitude, location.longitude)
    print(lat_long)

    ADDRESSES[user] = location.address
    print(ADDRESSES)

    if data['isDriver'][entry] == "1":
      drivers.append((user, lat_long))
    else:
      non_drivers.append((user, lat_long))

  # print(drivers)
  # print(non_drivers)
  return
  carpools = {}

  for driver in drivers:
    carpools[driver] = []

  def dist(entry1, entry2):
    return math.sqrt(((entry1[1][0] - entry2[1][0]) ** 2) + ((entry1[1][1] - entry2[1][1]) ** 2))

  for user in non_drivers:
    closest_distance = 999999
    closest_driver = ""
    for driver in drivers:
      distance = dist(driver, user)
      if distance < closest_distance:
        closest_distance = distance
        closest_driver = driver

    carpools[closest_driver].append(user)


  # print(carpools)

  for driver in carpools:
    temp_driver = driver
    while len(carpools[temp_driver]) > int(data['numSeats'][data['user'].index(temp_driver[0])]):
      closest_distance = 999999
      closest_new_driver = ""
      for new_driver in drivers:
        if new_driver != temp_driver:
          distance = dist(new_driver, temp_driver)
          if distance < closest_distance:
            closest_distance = distance
            closest_new_driver = new_driver

      closest_distance = 999999
      closest_non_driver = ""
      for non_driver in carpools[temp_driver]:
        distance = dist(non_driver, closest_new_driver)
        if distance < closest_distance:
          closest_distance = distance
          closest_non_driver = non_driver

      carpools[temp_driver].remove(closest_non_driver)
      carpools[closest_new_driver].append(closest_non_driver)

      #temp_driver = closest_new_driver

  # print(carpools)

  # carpools

  def get_all_paths(stops, path, paths):
      if not stops:
          paths.append(path)
          return

      for i, stop in enumerate(stops[:]):  # Make a copy of stops to iterate over
          next_path = path + [stop]  # Create a new path with the current stop
          remaining_stops = stops[:i] + stops[i+1:]  # Create a new list of stops without the current one
          get_all_paths(remaining_stops, next_path, paths)

      return paths

  def get_path_dist(path):
    total_dist = 0

    for index in range(1, len(path)):
      total_dist += dist(path[index - 1], path[index])

    return total_dist

  start = data['source'][0]

  geolocator = Nominatim(user_agent = "dhruvjwc@gmail.com")
  location = geolocator.geocode(start)
  lat_long = (location.latitude, location.longitude)

  ADDRESSES[start] = location.address

  START = (start, lat_long)

  shortest_paths = []

  for driver in carpools:
    stops = []
    for passenger in carpools[driver]:
      stops.append(passenger)

    if len(stops) > 0:
      paths = get_all_paths(stops, [], [])

      sorted_paths = []
      heapify(sorted_paths)

      for path in paths:
        path.insert(0, START)
        path.append(driver)
        heappush(sorted_paths, (get_path_dist(path), path))
    else:
      path = [START, driver]
      heappush(sorted_paths, (get_path_dist(path), path))

    shortest_path = heappop(sorted_paths)
    # print(shortest_path)
    shortest_paths.append(shortest_path[1])

  colors = ["red", "orange", "yellow", "green", "blue", "purple"]

  plt.xlabel("Longitude")
  plt.ylabel("Latitude")

  plt.scatter(START[1][1], START[1][0], c="pink", s=500)

  count = 0
  for driver in carpools:
    cc = (driver[1][1], driver[1][0])
    plt.scatter(cc[0], cc[1], c=colors[count], edgecolors="black", s=200)
    for passenger in carpools[driver]:
      myDist = dist(driver, passenger)
      plt.scatter(x=passenger[1][1], y=passenger[1][0], c=colors[count], s=50)
      #plt.plot([driver[1][1], passenger[1][1]], [driver[1][0], passenger[1][0]], color=colors[count], linestyle="-")
    count+=1

  for shortest_path in shortest_paths:
    for index in range(1, len(shortest_path)):
      plt.plot([shortest_path[index - 1][1][1], shortest_path[index][1][1]], [shortest_path[index - 1][1][0], shortest_path[index][1][0]], color="black", linestyle="--", label=str(index))
      midpointx = (shortest_path[index - 1][1][1] + shortest_path[index][1][1]) / 2
      midpointy = (shortest_path[index - 1][1][0] + shortest_path[index][1][0]) / 2
      plt.annotate("TJHSST", (START[1][1]-0.02, START[1][0] - 0.01))
  plt.savefig("output.png")
  #plt.show()

  start_time = datetime.now()

  o = open("output.txt", "w")

  for shortest_path in shortest_paths:

    specs = []

    specs.append("Driver: " + shortest_path[-1][0])
    start_address = ADDRESSES[start]
    specs.append("Starting Address: " + start_address)

    total_distance = 0
    total_time = 0

    for index in range(1, len(shortest_path)):

      address = ADDRESSES[shortest_path[index][0]]
      specs.append("Stop " + str(index) + " (" + shortest_path[index][0] + "): " + address)

      from_lat_long = str(shortest_path[index - 1][1][0]) + "," + str(shortest_path[index - 1][1][1])
      to_lat_long = str(shortest_path[index][1][0]) + "," + str(shortest_path[index][1][1])

      direction_result = gmaps_client.directions(from_lat_long, to_lat_long, mode="driving", avoid="ferries", departure_time=start_time)

      raw_distance = direction_result[0]['legs'][0]['distance']['value']
      raw_time = direction_result[0]['legs'][0]['duration']['value']
      distance = direction_result[0]['legs'][0]['distance']['text']
      time = direction_result[0]['legs'][0]['duration']['text']
      specs.append(distance)
      specs.append(time)

      total_distance += float(distance.split(" ")[0])
      total_time += int(time.split(" ")[0])

    specs.append("Total Distance: " + str(total_distance))
    specs.append("Total Time: " + str(total_time))
    specs.append("\n")

    o.write("\n".join(specs))

  o.close()

if __name__ == "__main__":
  main()

