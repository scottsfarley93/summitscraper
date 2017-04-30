import json
import sys
import re


def extractNumbers(s):
    extracted = re.findall(r'\d+', s)
    return len(extracted)


args = sys.argv

if len(args) != 2:
    print "An argument is required for this script."
    sys.exit()

infile = args[1]

openF = open(infile, 'r')
f = json.load(openF)

i = 0
while i < len(f):
    attributes = {}
    element = f[i]
    attr = element['attributes']
    attr_clean = filter(None, attr)
    print "-------"
    print len(attr_clean)
    print attr_clean

    firstNums = extractNumbers(attr_clean[0])
    if len(attr_clean) > 2:
        if (firstNums == 0):
            created = None
            location_raw = attr_clean[0]
            activities_raw = attr_clean[1]
        else:
            created = attr_clean[0]
            location_raw = attr_clean[1]
            activities_raw = attr_clean[2]

        location = location_raw.split("/")
        j = 0
        while j < len(location):
            location[j] = location[j].split(",")
            j += 1

        activities = activities_raw.split(",")
        j = 0
        while j < len(activities):
            activities[j] = re.findall('[A-Z][^A-Z]*', activities[j])
            j += 1

    elif len(attr_clean) == 2:
        location = None
        created = attr_clean[0]
        activities = None
        edited = attr_clean[1]
    elif len(attr_clean)== 1:
        location = None
        created = attr_clean[0]
        activities = None
        edited = None

    print activities



    i += 1

openF.close()

openF = open(infile, 'w')

json.dump(f, openF)