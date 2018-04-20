import argparse
import json
from elasticsearch import Elasticsearch
from elasticsearch_dsl import Search
esclient = Elasticsearch()

# Gather CLI arguments
parser = argparse.ArgumentParser()
parser.add_argument("--json", help="Path to JSON file with packages and versions")
parser.add_argument("--index", help="ElasticSearch index to search")
#parser.add_argument("--yaml", help="Path to YAML file with packages and versions")
parser.add_argument("-u", "--url", help="URL for ElasticSearch server to query")
parser.add_argument("-v", "--verbose", action="store_true", help="Give more verbose output")
args = parser.parse_args()

# Import JSON
with open(args.json) as json_data:
    parsed_json = json.load(json_data)

# Maybe use a collection dict?
# Break out the keyvalue maps
only_keyvalue = parsed_json['dependencyversions']

# Poll ElasticSearch for data

# Outputs
if args.json:
    print(json.dumps(only_keyvalue))
if args.url:
    print(args.url)