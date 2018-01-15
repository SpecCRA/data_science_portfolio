#!/usr/bin/env python

import re
import csv
import xml.etree.cElementTree as ET
import codecs
import pprint

import cerberus

import schema

OSM_PATH = "san_francisco.osm"
NODES_PATH = "nodes.csv"
NODE_TAGS_PATH = "nodes_tags.csv"
WAYS_PATH = "ways.csv"
WAY_NODES_PATH = "ways_nodes.csv"
WAY_TAGS_PATH = "ways_tags.csv"
SCHEMA = schema.schema

# Alameda de las Pulgas has many variations of capitalizations
alameda_regex = re.compile(r"(alameda\sde\sla\s)(pulgas)?", re.I)
# This is the same as the regex in the quizzes except I removed #
PROBLEMCHARS = re.compile(r'[=\+/&<>;\'"\?%$@\,\. \t\r\n]')
LOWER_COLON = re.compile(r'^([a-z]|_)+:([a-z]|_)+')
lower_case = re.compile("r[a-z]+")

# Make sure the fields order in the csvs matches the column order in the sql table schema
NODE_FIELDS = ['id', 'lat', 'lon', 'user', 'uid', 'version', 'changeset', 'timestamp']
NODE_TAGS_FIELDS = ['id', 'key', 'value', 'type']
WAY_FIELDS = ['id', 'user', 'uid', 'version', 'changeset', 'timestamp']
WAY_TAGS_FIELDS = ['id', 'key', 'value', 'type']
WAY_NODES_FIELDS = ['id', 'node_id', 'position']


"""
Each dictionary stores corrections to the respective street name, street to replace,
amenity, shop, or cuisine value from the auditing portion.
"""

street_corrections = {
        "Ctr": "Center",
        "Ave": "Avenue",
        "Ave.": "Avenue",
        "Avenie": "Avenue",
        "avenue": "Avenue",
        "Blvd": "Boulevard",
        "Blvd.": "Boulevard",
        "Dr": "Drive",
        "Dr.": "Drive",
        "Hwy": "Highway",
        "street": "Street",
        "St": "Street",
        "St.": "Street",
        "Plz": "Plaza"
         }

street_replacements = {
        "Van Ness": "Van Ness Avenue",
        "MILLSBRAE AVE": "Millsbrae Avenue",
        "MacDonald": "MacDonald Avenue",
        "3605 Telegraph": "3605 Telegraph Avenue",
        "Cesar Chavez St St": "Cesar Chavez Street",
        "Hyde": "Hyde Street",
        "King": "King Street",
        "Vallejo": "Vallejo Street",
        "broadway": "Broadway",
        "townsend street": "Townsend Street",
        "New Montgomery": "New Montgomery Street"
        }

amenities_corrections = {
        "car_sharing": "car_share",
        "community_centre": "community_center",
        "dancing_school": "dance_school",
        "fountian": "fountain" 
        }

shops_corrections = {
        "hairdresser": "hair_salon",
        "nail_salon": "nails",
        "bail_service": "bail_bond",
        "clothing": "clothes",
        "confectionary": "confectionery",
        "herbalist": "herbs",
        "herb": "herbs",
        "pet_store": "pet",
        "pet_supply": "pet",
        "outdoor_water_sports_and_swim": "outdoor",
        "beauty_products": "beauty",
        "fishing": "fish",
        "floor": "flooring",
        "garden_centre": "garden_center",
        "framing": "frame",
        "pawn": "pawnbroker",
        "thift_store": "thrift",
        "appliance": "appliances",
        "bathroom_furnishing": "bathroom_furnishings",
        "craft": "crafts",
        "rug": "rugs",
        "sport": "sports",
        "vitamin": "vitamins"
        }

cuisines_corrections = {
        "subs/sandwiches": "sandwiches",
        "dimsum": "dim_sum",
        "coffee1": "coffee",
        "coffee_shop": "coffee",
        "bubble_tea": "boba",
        "korean_food": "korean",
        "vietnamnese": "vietnamese", 
        "bbq": "barbecue",
        "doughnut": "donuts",
        "lao": "laotian",
        "california": "californian",
        "homemade_ice_cream": "ice_cream",
        "frozen_yoghurt": "frozen_yogurt",
        "guatamalen": "guatamalan",
        "hawaian": "hawaiian",
        "mexican_food": "mexican",
        "burger": "burgers",
        "burittos": "burrito",
        "crepe": "crepes",
        "donut": "donuts",
        "donut_shop": "donuts",
        "hot_dog": "hot_dogs",
        "hotdog": "hot_dogs",
        "noodle": "noodles",
        "salad": "salads",
        "sandwich": "sandwiches",
        "smoothie": "smoothies",
        "soup": "soups",
        "taco": "tacos"
        }

direction_storage = {
        "N": "North",
        "S": "South",
        "E": "East",
        "W": "West",
        "NE": "Northeast",
        "NW": "Northwest",
        "SE": "Southeast",
        "SW": "Southwest"
        }

"""
When creating your function to clean files, make sure you write in these steps.
1. Lower strings so everything is lower case
2. Replace all spaces with underscores
3. Check for special cases
4. Check to see if you need to convert to plurals
5. Check for special cases to skip or replace
6. Then check in dictionaries for each case
7. Remember with subcategories, just take the first one (split on ;)
"""

def clean_abbrev(word_list):
    """
    Checks and replaces a string for street or directional abbreviations with its
    full name. The third function is to correct any street names that are listed 
    in all lower case. Its purpose is to give the street names consistency. 
    This function is specifically for street names and nothing else.
    """

    for word in word_list:
        if word in street_corrections.keys():
            pos = words.index(word)
            words[pos] = street_corrections[word]
            string = " ".join(words)
            return string
        elif word in direction_storage.keys() and not string == "Avenue E":
            pos = words.index(word)
            words[pos] = direction_storage[word]
            string = " ".join(words)
            return string
        elif lower_case.search(word): # corrects bad capitaliztions
            pos = words.index(word)
            words[pos] = word.capitalize()
            string = " ".join(words)
            return string
        else:
            continue

def clean_street_name(string):
    """
    Clean street names with the dictionaries street_corrections and street_replacments.
    Fix variations in capitalizations in "Alameda de las Pulgas"
    Things in street_replacements are individually cleaned.
    street_corrections are in the string somewhere.
    -find its location after splitting into a list
    -remove then replace with dictionary value
    Remove "Wedemeyer", looks like it's a typo for Wedemeyer Bakery.
    """
    words = string.split()
    if string in street_replacements.keys():
        string = street_replacements[string]
        return string
    elif alameda_regex.search(string):
        string = "Alameda de las Pulgas"
        return string
    elif string == "Wedemeyer":
        pass
    else:
        try:
            clean_abbrev(words)
        except:
            return string

def prep_value(string):
    """
    Takes a string as an argument
    1. makes everything lower case
    2. replaces empty spaces with underscores
    3. split based on ; and take first value (but not barbecue;korean)
    4. also split on , and take first value

    This function deals with amenity, shop, and cuisine values.
    """
    working_string = string.lower()
    
    if " " in working_string:
        working_string = working_string.replace(" ", "_")

    elif ";" in working_string and not "barebecue;korean": #special case 
        working_string = working_string.split(";")[0]
        return working_string
    elif "," in working_string:
        working_string = working_string.split(",")[0]
        return working_string
    else:
        return working_string

def clean_amenity_value(string):
    """
    1. Remove addr:housenumber (the value), p, fixme, and yes -- return None
    2. use amenities_corretions dictionary for the typos and renaming
    """
    string = prep_value(string)
    if string == "addr:housenumber" or string == "p" or string == "fixme" \
            or string == "yes":
                return "Ignore value"
    elif string in amenities_corrections.keys():
        return amenities_corrections[string]
    else:
        return string

def clean_shop_cuisine(corrections_dict, string):
    """
    This is used for shop and cuisine values. The methods to clean these values
    are the same. First it calls the clean_value function and checks to see if
    there are corrections to be made. If not, this function will just return the
    original string.
    """
    new_string = prep_value(string)
    if new_string in corrections_dict.keys():
        return corrections_dict[new_string]
    else:
        return new_string

def process_key(key_string):
	# separates a key string value into its tag type or key value
    if ":" in key_string:
        indexed_string = key_string.find(":")
        tag_type = key_string[:indexed_string]
        new_key = key_string[indexed_string+1:]
        return [new_key, tag_type]
    else: 
        new_key = key_string
        tag_type = "regular"
        return [new_key, tag_type]

def shape_element(element, node_attr_fields=NODE_FIELDS, way_attr_fields=WAY_FIELDS,
                  problem_chars=PROBLEMCHARS, default_tag_type='regular'):

    node_attribs = {}
    way_attribs = {}
    way_nodes = []
    tags = []  # Handle secondary tags the same way for both node and way elements

    if element.tag == 'node':
        # Iterate through each node tag and add the appropriate names and values
        for attrName, attrValue in element.attrib.items():
            if attrName in NODE_FIELDS:
                node_attribs[attrName] = attrValue
        """
        Iterate through child tags to clean and add values I want to use after
        previously auditing.
        """
        for i in element.iter('tag'):
            temp_dict = {}
            if PROBLEMCHARS.search(i.attrib['k']):
                continue
            else:
            	cleaned_key = process_key(i.attrib['k'])[0]
            	cleaned_type = process_key(i.attrib['k'])[1]
                temp_dict['id'] = element.attrib['id']
                temp_dict['key'] = cleaned_key
                temp_dict['type'] = cleaned_type
                if i.attrib['k'] == "amenity":
                    if clean_amenity_value(i.attrib['v']):
                        temp_dict['value'] = clean_amenity_value(i.attrib['v'])
                    else:
                        continue
                elif cleaned_key == "street":
                    if clean_street_name(i.attrib['v']):
                        temp_dict['value'] = clean_street_name(i.attrib['v'])
                    else:
                        continue
                elif i.attrib['k'] == "shop":
                    if clean_shop_cuisine(shops_corrections, i.attrib['v']):
                        temp_dict['value'] = clean_shop_cuisine(shops_corrections, i.attrib['v'])
                    else:
                        continue
                elif i.attrib['k'] == "cuisine":
                    if clean_shop_cuisine(cuisines_corrections, i.attrib['v']):
                        temp_dict['value'] = clean_shop_cuisine(cuisines_corrections, i.attrib['v'])
                    else:
                        continue
                else:
                    temp_dict['value'] = i.attrib['v']
            tags.append(temp_dict)

        return {'node': node_attribs, 'node_tags': tags}

    elif element.tag == 'way':
        """
        The cleaning and writing of the way tags work the same as the node tags.
        I just haven't quite figured out how to put this into a function.
        And admittedly feel done with this part of the project.
        """
        for attrName, attrValue in element.attrib.items():
            if attrName in WAY_FIELDS:
                way_attribs[attrName] = attrValue

        for i in element.iter('tag'):
            temp_dict = {}
            if PROBLEMCHARS.search(i.attrib['k']):
                continue
            else:
            	cleaned_key = process_key(i.attrib['k'])[0]
            	cleaned_type = process_key(i.attrib['k'])[1]
                temp_dict['id'] = element.attrib['id']
                temp_dict['key'] = cleaned_key
                temp_dict['type'] = cleaned_type
                if i.attrib['k'] == "amenity":
                    if clean_amenity_value(i.attrib['v']):
                        temp_dict['value'] = clean_amenity_value(i.attrib['v'])
                    else:
                        continue
                elif cleaned_key == "street":
                    if clean_street_name(i.attrib['v']):
                        temp_dict['value'] = clean_street_name(i.attrib['v'])
                    else:
                        continue
                elif i.attrib['k'] == "shop":
                    if clean_shop_cuisine(shops_corrections, i.attrib['v']):
                        temp_dict['value'] = clean_shop_cuisine(shops_corrections, i.attrib['v'])
                    else:
                        continue
                elif i.attrib['k'] == "cuisine":
                    if clean_shop_cuisine(cuisines_corrections, i.attrib['v']):
                        temp_dict['value'] = clean_shop_cuisine(cuisines_corrections, i.attrib['v'])
                    else:
                        continue
                else:
                    temp_dict['value'] = i.attrib['v']
            tags.append(temp_dict)

        for counter, i in enumerate(element.iter('nd')):
            temp_dict = {}
            temp_dict['id'] = element.attrib['id']
            temp_dict['node_id'] = i.attrib['ref']
            temp_dict['position'] = counter
            way_nodes.append(temp_dict)


        return {'way': way_attribs, 'way_nodes': way_nodes, 'way_tags': tags}

# The following are functions from the case study quiz

def get_element(osm_file, tags=('node', 'way', 'relation')):
    """Yield element if it is the right type of tag"""

    context = ET.iterparse(osm_file, events=('start', 'end'))
    _, root = next(context)
    for event, elem in context:
        if event == 'end' and elem.tag in tags:
            yield elem
            root.clear()


def validate_element(element, validator, schema=SCHEMA):
    """Raise ValidationError if element does not match schema"""
    if validator.validate(element, schema) is not True:
        field, errors = next(validator.errors.iteritems())
        message_string = "\nElement of type '{0}' has the following errors:\n{1}"
        error_string = pprint.pformat(errors)
        
        raise Exception(message_string.format(field, error_string))


class UnicodeDictWriter(csv.DictWriter, object):
    """Extend csv.DictWriter to handle Unicode input"""

    def writerow(self, row):
        super(UnicodeDictWriter, self).writerow({
            k: (v.encode('utf-8') if isinstance(v, unicode) else v) for k, v in row.iteritems()
        })

    def writerows(self, rows):
        for row in rows:
            self.writerow(row)

def process_map(file_in, validate):
    """Iteratively process each XML element and write to csv(s)"""

    with codecs.open(NODES_PATH, 'w') as nodes_file, \
         codecs.open(NODE_TAGS_PATH, 'w') as nodes_tags_file, \
         codecs.open(WAYS_PATH, 'w') as ways_file, \
         codecs.open(WAY_NODES_PATH, 'w') as way_nodes_file, \
         codecs.open(WAY_TAGS_PATH, 'w') as way_tags_file:

        nodes_writer = UnicodeDictWriter(nodes_file, NODE_FIELDS)
        node_tags_writer = UnicodeDictWriter(nodes_tags_file, NODE_TAGS_FIELDS)
        ways_writer = UnicodeDictWriter(ways_file, WAY_FIELDS)
        way_nodes_writer = UnicodeDictWriter(way_nodes_file, WAY_NODES_FIELDS)
        way_tags_writer = UnicodeDictWriter(way_tags_file, WAY_TAGS_FIELDS)

        nodes_writer.writeheader()
        node_tags_writer.writeheader()
        ways_writer.writeheader()
        way_nodes_writer.writeheader()
        way_tags_writer.writeheader()

        validator = cerberus.Validator()

        for element in get_element(file_in, tags=('node', 'way')):
            el = shape_element(element)
            if el:
                if validate is True:
                    validate_element(el, validator)

                if element.tag == 'node':
                    nodes_writer.writerow(el['node'])
                    node_tags_writer.writerows(el['node_tags'])
                elif element.tag == 'way':
                    ways_writer.writerow(el['way'])
                    way_nodes_writer.writerows(el['way_nodes'])
                    way_tags_writer.writerows(el['way_tags'])


if __name__ == '__main__':
    # Note: Validation is ~ 10X slower. For the project consider using a small
    # sample of the map when validating.
    process_map(OSM_PATH, validate=False)

