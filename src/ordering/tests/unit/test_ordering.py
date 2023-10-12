import json
from datetime import datetime
from unittest import mock

import boto3
from moto import mock_dynamodb


@mock.patch.dict('os.environ', {
    "DYNAMODB_TABLE_NAME": "order",
})
@mock_dynamodb
def test_lambda_handler_get_all_orders(
    lambda_context
):
    from ...ordering import lambda_handler
    # Initialize the dynamo_db table
    dynamo_db = boto3.resource('dynamodb')

    # Define the table schema
    table_schema = {
        'TableName': 'order',
        'KeySchema': [
            {
                'AttributeName': 'userName',
                'KeyType': 'HASH'  # Partition key
            },
            {
                'AttributeName': 'orderDate',
                'KeyType': 'RANGE'  # Sort key
            }
        ],
        'AttributeDefinitions': [
            {
                'AttributeName': 'userName',
                'AttributeType': 'S'  # String
            },
            {
                'AttributeName': 'orderDate',
                'AttributeType': 'S'  # String
            }
        ],
        'BillingMode': 'PAY_PER_REQUEST',  # Pay per request
    }

    # Create the table
    table = dynamo_db.create_table(**table_schema)
    username = "test"
    order_date = datetime.utcnow().isoformat()

    item = {
        'userName': username,
        'orderDate': order_date,
        'data': {
                "firstName": "test",
                "lastName": "testinski",
                "address": "honolulu",
                "cardInfo": "5554443322",
                "totalPrice": "1820.0",
                "paymentMethod": "1",
                "items": [
                    {
                        "quantity": "2",
                        "color": "Red",
                        "productId": "2266628b-ff81-4a9f-a82d-8c46766aa122",
                        "price": "950.00",
                        "productName": "IPhone X"
                    },
                    {
                        "quantity": "1",
                        "color": "Blue",
                        "productId": "c4f49ceb-b1d4-4b2b-bbae-31f4e024b9d5",
                        "price": "870.00",
                        "productName": "Samsung 10"
                    }
                ],
                "email": "test@test.com"
            }
    }
    table.put_item(Item=item)

    event = {
        "httpMethod": "GET",
    }
    # Invoke the Lambda function
    response = lambda_handler(event, lambda_context)

    # Verify the response
    assert response["statusCode"] == 200
    res = json.loads(response["body"])
    assert res["body"][0]["data"]["items"] == item["data"]["items"]
    assert res["body"][0]["orderDate"] == order_date
    assert res["body"][0]["userName"] == username

    # Clean up
    table.delete()


@mock.patch.dict('os.environ', {
    "DYNAMODB_TABLE_NAME": "order",
})
@mock_dynamodb
def test_lambda_handler_get_order_by_username_and_date(
    lambda_context
):
    from ...ordering import lambda_handler
    # Initialize the dynamo_db table
    dynamo_db = boto3.resource('dynamodb')

    # Define the table schema
    table_schema = {
        'TableName': 'order',
        'KeySchema': [
            {
                'AttributeName': 'userName',
                'KeyType': 'HASH'  # Partition key
            },
            {
                'AttributeName': 'orderDate',
                'KeyType': 'RANGE'  # Sort key
            }
        ],
        'AttributeDefinitions': [
            {
                'AttributeName': 'userName',
                'AttributeType': 'S'  # String
            },
            {
                'AttributeName': 'orderDate',
                'AttributeType': 'S'  # String
            }
        ],
        'BillingMode': 'PAY_PER_REQUEST',  # Pay per request
    }

    # Create the table
    table = dynamo_db.create_table(**table_schema)
    username = "test"
    order_date = datetime.utcnow().isoformat()
    item = {
        'userName': username,
        'orderDate': order_date,
        'data': {
                "firstName": "test",
                "lastName": "testinski",
                "address": "honolulu",
                "cardInfo": "5554443322",
                "totalPrice": "1820.0",
                "paymentMethod": "1",
                "items": [
                    {
                        "quantity": "2",
                        "color": "Red",
                        "productId": "2266628b-ff81-4a9f-a82d-8c46766aa122",
                        "price": "950.00",
                        "productName": "IPhone X"
                    },
                    {
                        "quantity": "1",
                        "color": "Blue",
                        "productId": "c4f49ceb-b1d4-4b2b-bbae-31f4e024b9d5",
                        "price": "870.00",
                        "productName": "Samsung 10"
                    }
                ],
                "email": "test@test.com"
            }
    }
    table.put_item(Item=item)

    event = {
        "httpMethod": "GET",
        "pathParameters": {
            "userName": username,
        },
        "queryStringParameters": {
            "orderDate": order_date
        }
    }
    # Invoke the Lambda function
    response = lambda_handler(event, lambda_context)

    # Verify the response
    assert response["statusCode"] == 200
    res = json.loads(response["body"])
    assert res["body"]["data"]["items"] == item["data"]["items"]
    assert res["body"]["orderDate"] == order_date
    assert res["body"]["userName"] == username

    # Clean up
    table.delete()


@mock.patch.dict('os.environ', {
    "DYNAMODB_TABLE_NAME": "order",
})
@mock_dynamodb
def test_lambda_handler_wrong_route(
    lambda_context
):
    from ...ordering import lambda_handler
    # Initialize the dynamo_db table
    dynamo_db = boto3.resource('dynamodb')

    # Define the table schema
    table_schema = {
        'TableName': 'order',
        'KeySchema': [
            {
                'AttributeName': 'userName',
                'KeyType': 'HASH'  # Partition key
            },
            {
                'AttributeName': 'orderDate',
                'KeyType': 'RANGE'  # Sort key
            }
        ],
        'AttributeDefinitions': [
            {
                'AttributeName': 'userName',
                'AttributeType': 'S'  # String
            },
            {
                'AttributeName': 'orderDate',
                'AttributeType': 'S'  # String
            }
        ],
        'BillingMode': 'PAY_PER_REQUEST',  # Pay per request
    }

    # Create the table
    table = dynamo_db.create_table(**table_schema)

    event = {
        "httpMethod": "PATCH",
    }
    # Invoke the Lambda function
    response = lambda_handler(event, lambda_context)

    # Verify the response
    assert response["statusCode"] == 400

    # Clean up
    table.delete()


