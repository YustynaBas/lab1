import geopy
import geopy.distance
import folium
import time
from geopy.geocoders import Nominatim
from geopy.extra.rate_limiter import RateLimiter
import argparse


parser = argparse.ArgumentParser(description='Arguments')
parser.add_argument('year' , help = "Enter a year you would like to have a map for:")
parser.add_argument('lat' , help = "Enter your current location latitude:")
parser.add_argument("long" , help= "Enter your current location longtitude:")
parser.add_argument("path" , help="Enter path to your dataset")
arguments = parser.parse_args()
year = arguments.year
lat = float(arguments.lat)
long = float(arguments.long)
path =  arguments.path
current_location = tuple([lat, long])



def open_file(path):
    """
    (str) -> (list)
    this function opens a file from which we read 
    needed information
    
    """
    lst = []
    with open(path, encoding='utf-8', errors='ignore') as f:
        line = f.readline()
        while not line.startswith("=============="):
            line = f.readline()
        for line in f:
            if '{' in line:
                ind_start, ind_last = line.find('{'), line.find('}')
                line = line[:ind_start- 1] + line[ind_last + 1:]
            ind = line[::-1].find('(')
            if line.find("(") != len(line) - ind - 1:
                line = line[:len(line) - ind - 1]
            lst.append(line.strip().split())
    return lst
film_list = open_file(path)


def finding_year_films(film_list, year):
    """
    (list, str) -> (list)
    this function creates a list of films that were casted in the
    year user wants to have
    """
    year_list = []
    year = "(" + year + ")"
    for i in film_list:
        if year in i:
            year_list.append(i)
    year_list_2 = []
    for j in year_list:
        for l in j:
            if '}' in l:
                ind1 = j.index(l)
                year_list_2.append((j[:ind1 + 1], n))
            elif ')' in l:
                ind2 = j.index(l)
                n = j[:ind2 + 1] + [" ".join(j[ind2 + 1:])]
                year_list_2.append(n)
    return year_list_2
year_list_2 = finding_year_films(film_list, year)


def create_location(year_list_2):
    """
    (list) -> (list)
    this function creates a list of films and thaeir locations
    as latitude and longtitude
    """
    geolocator = Nominatim(user_agent="main.py")
    geocode = RateLimiter(geolocator.geocode, min_delay_seconds=1)
    location_lst = []
    for i in year_list_2:
        location = geolocator.geocode(i[-1])
        if location != None:
            location_lst.append((i[0], (location.latitude, location.longitude), i[-1]))
    return location_lst
location_lst = create_location(year_list_2)


def find_nearest_ten(location_lst, current_location):
    """
    (list, str) -> (list)
    this function finds the nearest ten films to the location
    that was entered by user
    """
    len_list = []
    for i in location_lst:
        length = str(geopy.distance.geodesic(current_location, i[1]))
        length = length.replace(' km', '')
        len_list.append((i[0], float(length), i[1], i[2]))
    len_list = sorted(len_list, key = lambda x: x[1])
    return len_list[:9]
len_list = find_nearest_ten(location_lst, current_location)


m = folium.Map(location=list(current_location), zoom_start=11)
first_layer = folium.FeatureGroup(name='My current location')
first_layer.add_child(folium.Marker(list(current_location), popup='my_point', tooltip= "Hello World"))
second_layer = folium.FeatureGroup(name='Films near me')
for i in len_list:
    second_layer.add_child(folium.CircleMarker(list(i[2]), radius = 10, popup=i[0], color = "red", tooltip=i[3]))
third_layer = folium.FeatureGroup(name='Five highest mountains')
third_layer.add_child(folium.Marker([27.988056, 86.925278], popup='Everest', tooltip= "Hello World"))
third_layer.add_child(folium.Marker([35.881389, 76.513333], popup='K2', tooltip="Hello World"))
third_layer.add_child(folium.Marker([27.703333, 88.1475], popup='Kangchenjunga', tooltip="Hello World"))
third_layer.add_child(folium.Marker([27.961667, 86.933056], popup='Lhotse', tooltip="Hello World"))
third_layer.add_child(folium.Marker([27.889722, 87.088889], popup='Makalu', tooltip="Hello World"))
m.add_child(first_layer)
m.add_child(second_layer)
m.add_child(third_layer)
m.add_child(folium.LayerControl())
m.save("map.html")


