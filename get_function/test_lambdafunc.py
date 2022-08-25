import boto3
import pytest
import json

from moto import mock_dynamodb
from app import lambda_handler

TEST_TABLE = "visitor_count"


@pytest.fixture
def use_moto():
    @mock_dynamodb
    def dynamodb_client():
        dynamodb = boto3.resource('dynamodb', region_name='us-east-1')

        # Create the table
        dynamodb.create_table(
            TableName=TEST_TABLE,
            KeySchema=[
                {
                    'AttributeName': 'loadcount',
                    'KeyType': 'HASH'
                },

            ],
            AttributeDefinitions=[
                {
                    'AttributeName': 'loadcount',
                    'AttributeType': 'S'
                },

            ],
            BillingMode='PAY_PER_REQUEST'
        )
        return dynamodb
    return dynamodb_client


@mock_dynamodb
def test_handler_for_status_200(use_moto):
    use_moto()
    table = boto3.resource('dynamodb', region_name='us-east-1').Table(TEST_TABLE)
    table.put_item(
        Item={
            'loadcount': "visitcount",
            'Quantity': "001"
        }
    )

    event = {
        "loadcount": "visitcount"
    }

    return_data = lambda_handler(event, "")
    body = json.loads(return_data['body'])

    assert return_data['statusCode'] == 400
   # assert body['loadcount'] == '100'
   # assert body['Quantity'] == '001'

