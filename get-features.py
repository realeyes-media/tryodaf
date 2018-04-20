import argparse
import json
from elasticsearch import Elasticsearch
from elasticsearch_dsl import Search
client = Elasticsearch()

# Gather CLI arguments
parser = argparse.ArgumentParser()
parser.add_argument("-i", "--input", help="Path to JSON file with packages and versions")
parser.add_argument("-u", "--url", help="URL for ElasticSearch server to query")
parser.add_argument("-v", "--verbose", action="store_true", help="Give more verbose output")
args = parser.parse_args()

# Do things
if args.input:
    print(args.input)
if args.url:
    print(args.url)