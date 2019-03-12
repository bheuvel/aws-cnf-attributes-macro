from json import dumps, loads
import copy
import requests
import re


def valid_tag_string(tag):
    rex = re.compile(r"^[a-zA-Z0-9+\-=._:/@ ]+$")
    return rex.match(tag) is not None


def retrieve_cnf():
    fact = ""
    count = 0

    while not valid_tag_string(fact):
        count += 1
        if count >= 10:
            fact = 'Chuck Norris does infinite loops in 4 seconds.'
            break
        content = requests.get(
            'http://api.icndb.com/jokes/random?limitTo=[nerdy]').text
        fact = loads(content)['value']['joke']

    return fact


def set_tag(tags, key, value, overwrite=False):
    entry_found = False
    for entry in tags:
        if entry['Key'] == key:
            entry_found = True
            if overwrite:
                entry['Value'] = value
    if not entry_found:
        tags += [{'Key': key, 'Value': value}]
    return tags


def initialize_tags_hierarchy(resource):
    # Create empty hierarchy ['Properties']['Tags'] if no Properties and/or Tags present
    resource = {**{'Properties': {}}, **resource}
    resource['Properties'] = {**{'Tags': []}, **resource['Properties']}
    return resource


def manage_tags(resource):
    resource = initialize_tags_hierarchy(resource)
    tags = resource["Properties"]["Tags"]

    # Enforce tags or provide defaults
    tags = set_tag(tags, "Project", "Some default project code")
    tags = set_tag(tags, "CostCenter", "Some default cost center code")
    tags = set_tag(tags, "ChuckNorrisFact", retrieve_cnf(), overwrite=True)

    resource["Properties"]["Tags"] = tags
    return resource


def process_template(template):
    new_template = copy.deepcopy(template)
    status = "anything_but_success_is_failure"

    for name, resource in new_template["Resources"].items():
        new_template["Resources"][name] = manage_tags(resource)

    status = "success"
    return status, new_template


def lambda_handler(event, context):

    print(f"Event data: {dumps(event)}")

    result = process_template(event["fragment"])

    return {"requestId": event["requestId"], "status": result[0], "fragment": result[1]}
