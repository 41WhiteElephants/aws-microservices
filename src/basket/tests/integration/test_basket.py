import json

import boto3
import requests


def test_lambda_handler_get_all_baskets(
    api_url
):
    # Initialize the DynamoDB table
    dynamo_db = boto3.resource("dynamodb")
    table = dynamo_db.Table("basket")
    item = {
      "userName": "test_user",
      "items": [
        {
          "quantity": "2",
          "color": "Red",
          "price": "950.00",
          "productId": "2266628b-ff81-4a9f-a82d-8c46766aa122",
          "productName": "IPhone X"
        },
        {
          "quantity": "1",
          "color": "Blue",
          "price": "870.00",
          "productId": "c4f49ceb-b1d4-4b2b-bbae-31f4e024b9d5",
          "productName": "Samsung 10"
        }
      ]
    }
    item2 = {
        "userName": "test_user2",
        "items": [
            {
                "quantity": "1",
                "color": "Red",
                "price": "950.00",
                "productId": "2266628b-ff81-4a9f-a82d-8c46766aa122",
                "productName": "IPhone X"
            },
            {
                "quantity": "2",
                "color": "Blue",
                "price": "870.00",
                "productId": "c4f49ceb-b1d4-4b2b-bbae-31f4e024b9d5",
                "productName": "Samsung 10"
            }
        ]
    }
    table.put_item(Item=item)
    table.put_item(Item=item2)

    # Invoke the Lambda function
    url = f"{api_url}/basket"
    response = requests.get(url)
    # Verify the response
    assert response.status_code == 200

    # Clean up before asserts to make sure db is cleared
    key = {
        'userName': item["userName"]
    }
    key2 = {
        'userName': item2["userName"]
    }

    table.delete_item(Key=key)
    table.delete_item(Key=key2)

    response_data = response.json()
    assert item in response_data["body"]
    assert item2 in response_data["body"]


def test_lambda_handler_get_basket_by_username(
    api_url
):
    # Initialize the DynamoDB table
    dynamo_db = boto3.resource("dynamodb")
    table = dynamo_db.Table("basket")
    item = {
      "userName": "test_user",
      "items": [
        {
          "quantity": "2",
          "color": "Red",
          "price": "950.00",
          "productId": "2266628b-ff81-4a9f-a82d-8c46766aa122",
          "productName": "IPhone X"
        },
        {
          "quantity": "1",
          "color": "Blue",
          "price": "870.00",
          "productId": "c4f49ceb-b1d4-4b2b-bbae-31f4e024b9d5",
          "productName": "Samsung 10"
        }
      ]
    }

    table.put_item(Item=item)

    # Invoke the Lambda function
    url = f"{api_url}/basket/{item['userName']}"
    response = requests.get(url)
    # Verify the response
    assert response.status_code == 200

    # Clean up before asserts to make sure db is cleared
    key = {
        'userName': item["userName"]
    }

    table.delete_item(Key=key)

    response_data = response.json()
    assert item == response_data["body"]


def test_lambda_handler_post_basket(
    api_url
):
    dynamo_db = boto3.resource("dynamodb")
    table = dynamo_db.Table("basket")
    item = {
      "userName": "test_user",
      "items": [
        {
          "quantity": "2",
          "color": "Red",
          "price": "950.00",
          "productId": "2266628b-ff81-4a9f-a82d-8c46766aa122",
          "productName": "IPhone X"
        },
        {
          "quantity": "1",
          "color": "Blue",
          "price": "870.00",
          "productId": "c4f49ceb-b1d4-4b2b-bbae-31f4e024b9d5",
          "productName": "Samsung 10"
        }
      ]
    }

    url = f"{api_url}/basket"
    response = requests.post(url, data=json.dumps(item))
    # Verify the response
    assert response.status_code == 200

    # Clean up before asserts to make sure db is cleared
    key = {
        'userName': item["userName"]
    }
    db_data = table.get_item(Key=key)
    db_item = db_data["Item"]
    table.delete_item(Key=key)

    assert item == db_item


def test_lambda_handler_post_basket_checkout(
    api_url
):
    dynamo_db = boto3.resource("dynamodb")
    table = dynamo_db.Table("basket")
    item = {
        "userName": "test_user",
        "items": [
            {
                "quantity": "2",
                "color": "Red",
                "price": "950.00",
                "productId": "2266628b-ff81-4a9f-a82d-8c46766aa122",
                "productName": "IPhone X"
            },
            {
                "quantity": "1",
                "color": "Blue",
                "price": "870.00",
                "productId": "c4f49ceb-b1d4-4b2b-bbae-31f4e024b9d5",
                "productName": "Samsung 10"
            }
        ]
    }
    table.put_item(Item=item)
    body = {
        "userName": "test_user",
        "totalPrice": 0,
        "firstName": "test",
        "lastName": "testinski",
        "email": "test@test.com",
        "address": "honolulu",
        "cardInfo": "5554443322",
        "paymentMethod": 1
        }

    url = f"{api_url}/basket/checkout"
    response = requests.post(url, data=json.dumps(body))
    # Verify the response
    assert response.status_code == 200

    # Clean up before asserts to make sure db is cleared
    key = {
        'userName': item["userName"]
    }
    db_data = table.get_item(Key=key)
    assert "Item" not in db_data

    table = dynamo_db.Table("order")
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


def test_lambda_handler_delete_basket(
    api_url
):
    dynamo_db = boto3.resource("dynamodb")
    table = dynamo_db.Table("basket")
    item = {
      "userName": "test_user",
      "items": [
        {
          "quantity": "2",
          "color": "Red",
          "price": "950.00",
          "productId": "2266628b-ff81-4a9f-a82d-8c46766aa122",
          "productName": "IPhone X"
        },
        {
          "quantity": "1",
          "color": "Blue",
          "price": "870.00",
          "productId": "c4f49ceb-b1d4-4b2b-bbae-31f4e024b9d5",
          "productName": "Samsung 10"
        }
      ]
    }
    table.put_item(Item=item)
    url = f"{api_url}/basket/checkout"
    response = requests.delete(url)
    # Verify the response
    assert response.status_code == 200
