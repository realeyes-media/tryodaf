import argparse
import json
import requests

#### Gather CLI arguments
# Requres a PR message to be passed in as a text file to --prmessage
parser = argparse.ArgumentParser()
parser.add_argument("--prmessage", help="File path to a newline separated PR description", required=True)
parser.add_argument("--outputfile", help="Name of JSON file to output results", default="output.json")
args = parser.parse_args()

pr_input_file = open(args.prmessage).read().splitlines()

#### Set up variables for format check
bug_formats = ['bugfix', 'Bugfix', 'bug', 'Bug']
feature_formats = ['feature', 'Feature']

# Track failure count and tracker
fail_count = 0
fail_list = []

# Set up Output format
parsed_pr = dict()
parsed_pr['featureorbugfix'] = ""
parsed_pr['featurenew'] = []
parsed_pr['bugfixnew'] = []
parsed_pr['ticketcustomer'] = []
parsed_pr['successorfailure'] = "Success"

print('Line check results:')
#### Check the PR Message
for x in pr_input_file:
    y = x.split(' - ')
#    print(y)
#    print(len(y))
#   Checking for which format is used
    if len(y)==3:
        print(len(y))
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
        print(len(y))
        for check in bug_formats:
            if check in y:
                parsed_pr['featureorbugfix'] = 'Bugfix'
                parsed_pr['bugfixnew'].append(y[1])
        for check in feature_formats:
            if check in y:
                parsed_pr['featureorbugfix'] = 'Feature'
                parsed_pr['featurenew'].append(y[1])
    elif len(y)>=4:
        print(len(y))
        fail_count = fail_count + 1
        fails = dict()
        fails['reason'] = "Too many fields supplied"
        fails['offending_entry'] = y
        fail_list.append(fails)
    elif len(y)==1 and not y[0].strip():
        print('Skipping empty line')
    elif len(y)==1:
        print(len(y))
        fail_count = fail_count + 1
        fails = dict()
        fails['reason'] = "Only one field supplied"
        fails['offending_entry'] = y
        fail_list.append(fails)
    else:
        print(y + 'is not a valid line, but we wont count it as a failure')

print()

#### Output
if fail_count>0:
    print('Number of failures:' + str(fail_count))
    fail_response = dict()
    fail_response['successorfailure'] = "Failure"
    fail_response['failure_list'] = fail_list
    print(json.dumps(fail_response))
    with open(args.outputfile, 'w') as f:
        json.dump(fail_response, f)
else:
    print(json.dumps(parsed_pr))
    with open(args.outputfile, 'w') as f:
        json.dump(parsed_pr, f)
#print(parsed_pr)

#print(type(pr_input_file))
#print(pr_input_file)