import json
from datetime import datetime
from unittest import mock

import boto3
import requests
from moto import mock_dynamodb


def test_lambda_handler_get_all_orders(
    api_url
):
    # Initialize the DynamoDB table
    dynamo_db = boto3.resource("dynamodb")
    table = dynamo_db.Table("order")

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

    # Invoke the Lambda function
    url = f"{api_url}/order"
    response = requests.get(url)
    # Verify the response
    assert response.status_code == 200

    db_data = table.scan()
    # clean before error might occur in asserts
    assert "Items" in db_data

    db_order = db_data["Items"][0]
    key = {
        'userName': db_order["userName"],
        'orderDate': db_order["orderDate"],
    }
    table.delete_item(Key=key)
    assert item["userName"] == db_order["userName"]


def test_lambda_handler_get_order_by_username_and_date(
    api_url
):
    # Initialize the DynamoDB table
    dynamo_db = boto3.resource("dynamodb")
    table = dynamo_db.Table("order")
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
    url = f"{api_url}/order/{username}?orderDate={order_date}"
    response = requests.get(url)
    # Verify the response
    assert response.status_code == 200

    db_data = table.scan()
    # clean before error might occur in asserts
    assert "Items" in db_data

    db_order = db_data["Items"][0]
    key = {
        'userName': db_order["userName"],
        'orderDate': db_order["orderDate"],
    }
    table.delete_item(Key=key)
    assert item["userName"] == db_order["userName"]
