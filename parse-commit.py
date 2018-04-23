import argparse
import json

# Gather CLI arguments
parser = argparse.ArgumentParser()
parser.add_argument("--input", help="Newline separated commit message")
args = parser.parse_args()

# Read STDIN
input_file = open(args.input).read().splitlines()

# Set up Output format
field_split = dict()
field_split['featureorbugfix'] = ""
field_split['featurenew'] = []
field_split['featuretotal'] = []
field_split['bugfixnew'] = []
field_split['bugfixtotal'] = []
field_split['ticketcustomer'] = []


bug_formats = ['bugfix', 'Bugfix', 'bug', 'Bug']
feature_formats = ['feature', 'Feature']

for x in input_file:
    y = x.split(' - ')
    print(y)
    print(len(y))
#   Checking for which format is used
    if len(y)==3:
        for check in bug_formats:
            if check in y:
                field_split['featureorbugfix'] = 'Bugfix'
                field_split['bugfixnew'].append(y[2])
                field_split['ticketcustomer'].append(y[0])
        for check in feature_formats:
            if check in y:
                field_split['featureorbugfix'] = 'Feature'
                field_split['featurenew'].append(y[2])
                field_split['ticketcustomer'].append(y[0])
    elif len(y)==2:
        for check in bug_formats:
            if check in y:
                field_split['featureorbugfix'] = 'Bugfix'
                field_split['bugfixnew'].append(y[1])
        for check in feature_formats:
            if check in y:
                field_split['featureorbugfix'] = 'Feature'
                field_split['featurenew'].append(y[1])
    else:
        print('Not a valid line')

print(json.dumps(field_split))