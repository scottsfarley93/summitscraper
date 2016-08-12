__author__ = 'scottsfarley'
import json
from pprint import pprint
f = open("summitpost.json")
dataset = json.load(f)

print "There are ", len(dataset), " routes in your dataset."
routes_with_data = []
routes_without_data = []
parentURLs = []
routeURLs = []
parents = []
for item in dataset:
    route = item['route']
    parent = item['parent']
    if 'Activities' in route.keys():
        routes_with_data.append(route)
        route['parentURL'] = parent['url']
        routeURLs.append(route['url'])

    else:
        routes_without_data.append(route)
    if parent['url'] not in parentURLs:
        parentURLs.append(parent['url'])
        parents.append(parent)



for parent in parents:
    parent['routes'] = []
    parentURL = parent['url']
    for route in routes_with_data:
        if route['parentURL'] == parentURL:
            parent['routes'].append(route)
        route['images'] = set(route['images'])
    parent['images'] = set(parent['images'])




pprint(parents)
