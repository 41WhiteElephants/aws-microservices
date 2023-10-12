import json
import uuid
from unittest import mock

import boto3
from moto import mock_dynamodb


@mock.patch.dict('os.environ', {
    "DYNAMODB_TABLE_NAME": "product",
})
@mock_dynamodb
def test_lambda_handler_get_all_products(
    lambda_context
):
    from ...product import lambda_handler
    # Initialize the dynamo_db table
    dynamo_db = boto3.resource("dynamodb")
    table = dynamo_db.create_table(
        TableName="product",
        KeySchema=[{"AttributeName": "id", "KeyType": "HASH"}],
        AttributeDefinitions=[{"AttributeName": "id", "AttributeType": "S"}],
        BillingMode="PAY_PER_REQUEST"
    )
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
    items_list = [item, item2]
    table.put_item(Item=item)
    table.put_item(Item=item2)

    event = {
        "httpMethod": "GET",
    }
    # Invoke the Lambda function
    response = lambda_handler(event, lambda_context)

    # Verify the response
    assert response["statusCode"] == 200
    res = json.loads(response["body"])
    assert res["body"] == items_list

    # Clean up
    table.delete()


@mock.patch.dict('os.environ', {
    "DYNAMODB_TABLE_NAME": "product",
})
@mock_dynamodb
def test_lambda_handler_get_product_by_id(
    lambda_context
):
    from ...product import lambda_handler
    # Initialize the DynamoDB table
    dynamo_db = boto3.resource("dynamodb")
    table = dynamo_db.create_table(
        TableName="product",
        KeySchema=[{"AttributeName": "id", "KeyType": "HASH"}],
        AttributeDefinitions=[{"AttributeName": "id", "AttributeType": "S"}],
        BillingMode="PAY_PER_REQUEST"
    )
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

    event = {
        "httpMethod": "GET",
        "path": "/product",
        "pathParameters": {
            "id": product_id
        }
    }
    # Invoke the Lambda function
    response = lambda_handler(event, lambda_context)

    # Verify the response
    assert response["statusCode"] == 200
    assert "body" in response

    res = json.loads(response["body"])

    assert res["body"] == item

    # Clean up
    table.delete()


@mock.patch.dict('os.environ', {
    "DYNAMODB_TABLE_NAME": "product",
})
@mock_dynamodb
def test_lambda_handler_post_basket(
    lambda_context
):
    from ...product import lambda_handler
    # Initialize the DynamoDB table
    dynamo_db = boto3.resource("dynamodb")
    table = dynamo_db.create_table(
        TableName="product",
        KeySchema=[{"AttributeName": "id", "KeyType": "HASH"}],
        AttributeDefinitions=[{"AttributeName": "id", "AttributeType": "S"}],
        BillingMode="PAY_PER_REQUEST"
    )
    item = {
        "name": "Iphone 11",
        "description": "This phone is the company's biggest change to its flagship smartphone in years.",
        "imageFile": "product-2.png",
        "category": "Phone",
        "price": "950.00"
    }

    event = {
        "httpMethod": "POST",
        "path": "/product",
        "body": json.dumps(item)
    }
    # Invoke the Lambda function
    response = lambda_handler(event, lambda_context)

    # Verify the response
    assert response["statusCode"] == 200

    # Clean up
    table.delete()


@mock.patch.dict('os.environ', {
    "DYNAMODB_TABLE_NAME": "product",
})
@mock_dynamodb
def test_lambda_handler_put_basket(
    lambda_context
):
    from ...product import lambda_handler
    # Initialize the DynamoDB table
    dynamo_db = boto3.resource("dynamodb")
    table = dynamo_db.create_table(
        TableName="product",
        KeySchema=[{"AttributeName": "id", "KeyType": "HASH"}],
        AttributeDefinitions=[{"AttributeName": "id", "AttributeType": "S"}],
        BillingMode="PAY_PER_REQUEST"
    )
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
    new_img = "product-3.png"
    event = {
        "httpMethod": "PUT",
        "path": "/product",
        "body": json.dumps({"imageFile": new_img}),
        "pathParameters": {
            "id": product_id
        }
    }
    # Invoke the Lambda function
    response = lambda_handler(event, lambda_context)

    # Verify the response
    assert response["statusCode"] == 200

    # Clean up
    table.delete()


@mock.patch.dict('os.environ', {
    "DYNAMODB_TABLE_NAME": "product",
})
@mock_dynamodb
def test_lambda_handler_delete_product(
    lambda_context
):
    from ...product import lambda_handler
    # Initialize the DynamoDB table
    dynamo_db = boto3.resource("dynamodb")
    table = dynamo_db.create_table(
        TableName="product",
        KeySchema=[{"AttributeName": "id", "KeyType": "HASH"}],
        AttributeDefinitions=[{"AttributeName": "id", "AttributeType": "S"}],
        BillingMode="PAY_PER_REQUEST"
    )
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
    event = {
        "httpMethod": "DELETE",
        "path": "/product",
        "pathParameters": {
            "id": product_id
        }
    }
    # Invoke the Lambda function
    response = lambda_handler(event, lambda_context)

    # Verify the response
    assert response["statusCode"] == 200

    # Clean up
    table.delete()


@mock.patch.dict('os.environ', {
    "DYNAMODB_TABLE_NAME": "product",
})
@mock_dynamodb
def test_lambda_handler_wrong_route(
    lambda_context
):
    from ...product import lambda_handler
    # Initialize the DynamoDB table
    dynamo_db = boto3.resource("dynamodb")
    table = dynamo_db.create_table(
        TableName="product",
        KeySchema=[{"AttributeName": "id", "KeyType": "HASH"}],
        AttributeDefinitions=[{"AttributeName": "id", "AttributeType": "S"}],
        BillingMode="PAY_PER_REQUEST"
    )
    event = {
        "httpMethod": "PATCH",
        "path": "/product",
    }
    # Invoke the Lambda function
    response = lambda_handler(event, lambda_context)

    # Verify the response
    assert response["statusCode"] == 400

    # Clean up
    table.delete()
