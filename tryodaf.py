## Track yo (dang) features
# Requires Python 3.5+, ElasticSearch 6.2+, and all the args are required except the defaults.

import argparse
import json
import requests

#### Gather CLI arguments
# Requres a PR message to be passed in as a text file to --prmessage
parser = argparse.ArgumentParser()
parser.add_argument("--name", help="Name of this package or app", required=True)
parser.add_argument("--packageorapp", help="Is this a package or app?", required=True)
parser.add_argument("--version", help="The version of this package or app", required=True)
parser.add_argument("--commitdate", help="Date of this commit", required=True)
parser.add_argument("--commitmessage", help="Message of this commit", required=True)
parser.add_argument("--prmessage", help="File path to a newline separated PR description", required=True)
parser.add_argument("--json", help="Path to JSON file with package:version list", required=True)
parser.add_argument("--index", help="ElasticSearch index to search", required=True)
parser.add_argument("-u", "--url", help="URL for ElasticSearch server to query", required=True)
parser.add_argument("--changelog", help="The previous CHANGELOG in json format for loading in total values", required=True)
parser.add_argument("--doctype", help="ElasticSearch doc type to search. (default: doc)", default="doc")
parser.add_argument("--outputfile", help="Name of JSON file to output results", default="output.json")
#parser.add_argument("-v", "--verbose", action="store_true", help="Give more verbose output")
args = parser.parse_args()

# Structuring final output
final_json = dict()
final_json['name'] = args.name
final_json['packageorapp'] = args.packageorapp
final_json['version'] = args.version
final_json['commitdate'] = args.commitdate
final_json['commitmessage'] = args.commitmessage
final_json['featureorbugfix'] = ""
final_json['featurenew'] = []
final_json['featuretotal'] = []
final_json['bugfixtotal'] = []
final_json['bugfixnew'] = []
final_json['ticketcustomer'] = []
final_json['dependencyversions'] = []

#### Define a function to remove duplicates
def Remove(duplicate):
    final_list = []
    for num in duplicate:
        if num not in final_list:
            final_list.append(num)
    return final_list

#### Parse the PR Message into the fields we need 
# Read Input File and split by lines into a list
pr_input_file = open(args.prmessage).read().splitlines()

# Set up Output format
parsed_pr = dict()
parsed_pr['featureorbugfix'] = ""
parsed_pr['featurenew'] = []
parsed_pr['bugfixnew'] = []
parsed_pr['ticketcustomer'] = []


bug_formats = ['bugfix', 'Bugfix', 'bug', 'Bug']
feature_formats = ['feature', 'Feature']

for x in pr_input_file:
    y = x.split(' - ')
    print(y)
    print(len(y))
#   Checking for which format is used
    if len(y)==3:
        for check in bug_formats:
            if check in y:
                parsed_pr['featureorbugfix'] = 'Bugfix'
                parsed_pr['bugfixnew'].append(y[2])
                parsed_pr['ticketcustomer'].append(y[0])
        for check in feature_formats:
            if check in y:
                parsed_pr['featureorbugfix'] = 'Feature'
                parsed_pr['featurenew'].append(y[2])
                parsed_pr['ticketcustomer'].append(y[0])
    elif len(y)==2:
        for check in bug_formats:
            if check in y:
                parsed_pr['featureorbugfix'] = 'Bugfix'
                parsed_pr['bugfixnew'].append(y[1])
        for check in feature_formats:
            if check in y:
                parsed_pr['featureorbugfix'] = 'Feature'
                parsed_pr['featurenew'].append(y[1])
    else:
        print('Not a valid line')

#### Query ElasticSearch for dependency versions
# Declare the lists we need to return
feature_list = []
bug_list = []

# Import JSON files
with open(args.json, 'rb') as json_data:
    parsed_json = json.load(json_data)

with open(args.changelog, 'rb') as changelog_data:
    old_changelog = json.load(changelog_data)

# Get the package:version into dictionary pack_version
pack_version = {}
only_keyvalue = parsed_json['dependencyversions']
for stuff in only_keyvalue:
    pack_version.update({stuff["package"]:stuff["version"]})
print(json.dumps(pack_version))

# Get back features and bugs from ElasticSearch 6.2 for all packages
for pack,vers in pack_version.items():
    # Make an API request for ES data
#    print(args.url + "/" + args.index + "/" + args.doctype + "/_search?default_operator=AND&q=" + "name:" + "\"" + pack + "\"" + "+" + "version:" + vers)
    r = requests.get(args.url + "/" + args.index + "/" + args.doctype + "/_search?default_operator=AND&q=" + "name:" + "\"" + pack + "\"" + "+" + "version:" + vers)
    j = json.loads(r.text)
    # Navigate the nested JSON to get the data we want and add to list...check that number if anything breaks
    feature_list.extend(j['hits']['hits'][0]['_source']['featuretotal'])
    bug_list.extend(j['hits']['hits'][0]['_source']['bugfixtotal'])

# Remove duplicates
bugs = Remove(bug_list)
features = Remove(feature_list)

# Create a dictionary for the 2 lists and return as JSON
es_results = { "featuretotal": features, "bugfixtotal": bugs }

#### Add step parts together so we combine and remove duplicates all the step dictionaries
final_json['featureorbugfix'] = parsed_pr['featureorbugfix']
final_json['featurenew'] = parsed_pr['featurenew']
final_json['bugfixnew'] = parsed_pr['bugfixnew']
final_json['ticketcustomer'] = parsed_pr['ticketcustomer']
final_json['featuretotal'] = Remove(parsed_pr['featurenew'] + es_results['featuretotal'] + old_changelog['featuretotal'])
final_json['bugfixtotal'] = Remove(parsed_pr['bugfixnew'] + es_results['bugfixtotal'] + old_changelog['bugfixtotal'])
final_json['dependencyversions'] = parsed_json['dependencyversions']

#### Final Output
print(json.dumps(final_json))
with open(args.outputfile, 'w') as f:
    json.dump(final_json, f)