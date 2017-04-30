import json
import sys
import re


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
    # print "-------"
    # print len(attr_clean)
    # print attr_clean


    if len(attr_clean) == 2:
        created = attr_clean[0]
        edited = attr_clean[1]
        el_feet  = None 
        el_meters = None 
        hasGPXFile = False 
        location = ""

    if len(attr_clean) == 3:
        created = attr_clean[0]
        el_feet = None
        el_meters = None
        hasGPXFile = False
        location = attr_clean[1]
        edited = attr_clean[-1]

    elif len(attr_clean) == 4:
        if "ft/" in attr_clean[0]:
            created = attr_clean[1]
            el_feet = attr_clean[0]
            el_feet = int(el_feet.replace("ft/", ""))
            el_meters = attr_clean[1]
            el_meters = int(el_meters.replace("m", ""))
            hasGPXFile = False
            location = ""
        elif "m" in attr_clean[0]:
            created = attr_clean[1]
            el_feet = None
            el_meters = attr_clean[0]
            el_meters = int(el_meters.replace("m", ""))
            hasGPXFile = False
            location = attr_clean[2]
        else:
            created = attr_clean[0]
            el_feet = None
            el_meters = None
            hasGPXFile = True
            location = attr_clean[2]
        edited = attr_clean[-1]

    
    elif len(attr_clean) == 5:
        if "ft/" in attr_clean[0]:
            created = attr_clean[2]
            el_feet = attr_clean[0]
            el_feet = int(el_feet.replace("ft/", ""))
            el_meters = attr_clean[1]
            el_meters = int(el_meters.replace("m", ""))
            hasGPXFile = False
            location = attr_clean[3]
        else:
            created = attr_clean[1]
            el_feet = None
            el_meters = attr_clean[0]
            el_meters = int(el_meters.replace("m", ""))
            hasGPXFile = True
            location = attr_clean[2]
        edited = attr_clean[-1]

    elif len(attr_clean) == 6:
        created = attr_clean[2]
        el_feet = attr_clean[0]
        el_feet = int(el_feet.replace("ft/", ""))
        el_meters = attr_clean[1]
        el_meters = int(el_meters.replace("m", ""))
        hasGPXFile = True
        location = attr_clean[3]
        edited = attr_clean[-1]

    location = location.split("/")
    j = 0
    while j < len(location):
        # location = re.findall('[A-Z][a-z]*', location)
        location[j] = location[j].split(",")
        j += 1
    if el_meters is None and el_feet is not None:
        el_meters = el_feet * 0.3048000097536
    if el_feet is None and el_meters is not None:
        el_feet = el_meters * 3.2808399999999999785
    f[i]['location'] = location
    f[i]['elevation']= {
        "feet" : el_feet,
        "meters" : el_meters
    }
    f[i]["page"] ={
        "created" : created,
        "edited" : edited
    }
    f[i]["hasGPXFile"] = hasGPXFile
    del f[i]['attributes']
    i += 1

openF.close()

openF = open(infile, 'w')

json.dump(f, openF)