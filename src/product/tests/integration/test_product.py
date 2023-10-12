import json
import uuid

import boto3
import requests


def test_lambda_handler_get_all_products(
    api_url
):
    # Initialize the DynamoDB table
    dynamo_db = boto3.resource("dynamodb")
    table = dynamo_db.Table("product")
    item = {
        "id": str(uuid.uuid4()),
        "name": "Iphone 11",
        "description": "This phone is the company's biggest change to its flagship smartphone in years.",
        "imageFile": "product-2.png",
        "category": "Phone",
        "price": "950.00"
    }
    item2 = {
        "id": str(uuid.uuid4()),
        "name": "Samsung 10",
        "description": "This phone is the company's biggest change to its flagship smartphone in years.",
        "imageFile": "product-2.png",
        "category": "Phone",
        "price": "740.40"
    }
    table.put_item(Item=item)
    table.put_item(Item=item2)

    # Invoke the Lambda function
    url = f"{api_url}/product"
    response = requests.get(url)
    # Verify the response
    assert response.status_code == 200

    # Clean up before asserts to make sure db is cleared
    key = {
        'id': item["id"]
    }
    key2 = {
        'id': item2["id"]
    }

    table.delete_item(Key=key)
    table.delete_item(Key=key2)

    response_data = response.json()
    assert item in response_data["body"]
    assert item2 in response_data["body"]


def test_lambda_handler_get_product_by_id(
    api_url
):
    # Initialize the DynamoDB table
    dynamo_db = boto3.resource("dynamodb")
    table = dynamo_db.Table("product")
    item = {
        "id": str(uuid.uuid4()),
        "name": "Iphone 11",
        "description": "This phone is the company's biggest change to its flagship smartphone in years.",
        "imageFile": "product-2.png",
        "category": "Phone",
        "price": "950.00"
    }
    table.put_item(Item=item)

    # Invoke the Lambda function
    url = f"{api_url}/product/{item['id']}"
    response = requests.get(url)
    # Verify the response
    assert response.status_code == 200

    # Clean up before asserts to make sure db is cleared
    key = {
        'id': item["id"]
    }
    table.delete_item(Key=key)

    response_data = response.json()
    assert response_data["body"] == item


def test_lambda_handler_post_product(
    api_url
):
    # Initialize the DynamoDB table
    dynamo_db = boto3.resource("dynamodb")
    table = dynamo_db.Table("product")
    item = {
        "name": "Iphone 11",
        "description": "This phone is the company's biggest change to its flagship smartphone in years.",
        "imageFile": "product-2.png",
        "category": "Phone",
        "price": "950.00"
    }

    # Invoke the Lambda function
    url = f"{api_url}/product"
    response = requests.post(url, data=json.dumps(item))
    # Verify the response
    assert response.status_code == 200
    response = table.scan()
    assert "Items" in response
    db_product = response["Items"][0]
    # Clean up before asserts to make sure db is cleared
    key = {
        'id': db_product["id"]
    }
    table.delete_item(Key=key)

    db_product.pop("id")
    assert item == db_product


def test_lambda_handler_put_product(
    api_url
):
    # Initialize the DynamoDB table
    dynamo_db = boto3.resource("dynamodb")
    table = dynamo_db.Table("product")
    product_id = str(uuid.uuid4())
    item = {
        "id": product_id,
        "name": "Iphone 11",
        "description": "This phone is the company's biggest change to its flagship smartphone in years.",
        "imageFile": "product-2.png",
        "category": "Phone",
        "price": "950.00"
    }
    table.put_item(Item=item)

    # Invoke the Lambda function
    url = f"{api_url}/product/{product_id}"
    new_img = "product-3.png"
    response = requests.put(url, data=json.dumps({"imageFile": new_img}))
    # Verify the response
    assert response.status_code == 200
    key = {
        'id': product_id
    }
    res = table.get_item(Key=key)
    db_product = res["Item"]
    # Clean up before asserts to make sure db is cleared

    table.delete_item(Key=key)

    assert db_product["imageFile"] == new_img


def test_lambda_handler_delete_product(
    api_url
):
    # Initialize the DynamoDB table
    dynamo_db = boto3.resource("dynamodb")
    table = dynamo_db.Table("product")
    product_id = str(uuid.uuid4())
    item = {
        "id": product_id,
        "name": "Iphone 11",
        "description": "This phone is the company's biggest change to its flagship smartphone in years.",
        "imageFile": "product-2.png",
        "category": "Phone",
        "price": "950.00"
    }
    table.put_item(Item=item)

    # Invoke the Lambda function
    url = f"{api_url}/product/{product_id}"
    response = requests.delete(url)
    # Verify the response
    assert response.status_code == 200
