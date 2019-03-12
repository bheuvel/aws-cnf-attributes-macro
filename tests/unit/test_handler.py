from collections import namedtuple
import json

import pytest

from cnf_attributes_macro import app


@pytest.fixture()
def cfn_macro_call():
    return {
        "region": "eu-west-1",
        "accountId": "001122334455",
        "fragment": {
            "Resources": {
                "Bucket01": {"Type": "AWS::S3::Bucket"},
                "Bucket02": {
                    "Type": "AWS::S3::Bucket",
                    "Properties": {
                        "Tags": [
                            {"Key": "Project", "Value": "Project macro test"},
                            {"Key": "ChuckNorrisFact", "Value": "old fact"}
                        ]
                    },
                },
            },
        },
        "transformId": "001122334455::AttributesMacro",
        "params": {},
        "requestId": "12abc345-a1b2-3cde-1234-aa1b23c4d5e6",
        "templateParameterValues": {},
    }


@pytest.fixture()
def cfn_macro_return():
    return {"requestId": "$REQUEST_ID", "status": "$STATUS", "fragment": {"..."}}


@pytest.fixture()
def cfn_fact():
    return 'Chuck Norris does infinite loops in 4 seconds.'


def test_valid_tag_string():
    assert app.valid_tag_string("abc123") == True
    assert app.valid_tag_string("a-zA-Z0-9+-=._:/@ a-zA-Z0-9+-=._:/@ ") == True
    assert app.valid_tag_string("--x--") == True
    assert app.valid_tag_string("--,--") == False
    assert app.valid_tag_string("--#--") == False
    assert app.valid_tag_string("--*--") == False
    assert app.valid_tag_string("--&--") == False
    assert app.valid_tag_string("--!--") == False
    assert app.valid_tag_string("--$--") == False
    assert app.valid_tag_string("--%--") == False
    assert app.valid_tag_string("--(--") == False
    assert app.valid_tag_string("--{--") == False
    assert app.valid_tag_string("--[--") == False
    assert app.valid_tag_string("") == False


def test_retrieve_cfn(requests_mock):
    requests_mock.get(
        'http://api.icndb.com/jokes/random?limitTo=[nerdy]', text='{ "value": { "joke": "#" } }')
    assert app.retrieve_cnf() == 'Chuck Norris does infinite loops in 4 seconds.'


def test_lambda_handler(requests_mock, cfn_macro_call, cfn_fact):
    requests_mock.get(
        'http://api.icndb.com/jokes/random?limitTo=[nerdy]', text='{ "value": { "joke": "' + cfn_fact + '" } }')

    ret = app.lambda_handler(cfn_macro_call, "")
    assert ret["status"] == "success"
    assert ret["fragment"]["Resources"]["Bucket01"]["Properties"]["Tags"][2]["Key"] == "ChuckNorrisFact"
    assert ret["fragment"]["Resources"]["Bucket01"]["Properties"]["Tags"][2]["Value"] == cfn_fact
    assert ret["fragment"]["Resources"]["Bucket02"]["Properties"]["Tags"][1]["Key"] == "ChuckNorrisFact"
    assert ret["fragment"]["Resources"]["Bucket02"]["Properties"]["Tags"][1]["Value"] == cfn_fact
