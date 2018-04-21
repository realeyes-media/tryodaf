import argparse
import json
import requests

# Gather CLI arguments
parser = argparse.ArgumentParser()
parser.add_argument("--json", help="Path to JSON file with packages and versions")
parser.add_argument("--index", help="ElasticSearch index to search")
parser.add_argument("-u", "--url", help="URL for ElasticSearch server to query")
parser.add_argument("--doctype", help="ElasticSearch doc type to search. (default: doc)", default="doc")
parser.add_argument("-v", "--verbose", action="store_true", help="Give more verbose output")
args = parser.parse_args()

# Define a function to remove duplicates
def Remove(duplicate):
    final_list = []
    for num in duplicate:
        if num not in final_list:
            final_list.append(num)
    return final_list

# Declare the lists we need to return
feature_list = []
bug_list = []

# Import JSON
with open(args.json, 'rb') as json_data:
    parsed_json = json.load(json_data)

# Get the package:version into dictionary pack_version
pack_version = {}
only_keyvalue = parsed_json['dependencyversions']
for stuff in only_keyvalue:
    pack_version.update({stuff["package"]:stuff["version"]})

# Get back features and bugs from ElasticSearch 6.2 for all packages
for pack,vers in pack_version.items():
    # Make an API request for ES data
    r = requests.get(args.url + "/" + args.index + "/" + args.doctype + "/_search?default_operator=AND&q=" + "name:" + "\"" + pack + "\"" + "+" + "version:" + vers)
    j = json.loads(r.text)
    # Navigate the nested JSON to get the data we want and add to list...check that number if anything breaks
    feature_list.extend(j['hits']['hits'][0]['_source']['featuretotal'])
    bug_list.extend(j['hits']['hits'][0]['_source']['bugfixtotal'])

# Remove duplicates
bugs = Remove(bug_list)
features = Remove(feature_list)

# Create a dictionary for the 2 lists and return as JSON
combined_json = { "featuretotal": features, "bugfixtotal": bugs }
print(json.dumps(combined_json))