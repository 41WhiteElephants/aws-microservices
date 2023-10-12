import json
from unittest import mock

import boto3
from moto import mock_dynamodb, mock_events


@mock.patch.dict('os.environ', {
    "DYNAMODB_TABLE_NAME": "basket",
    "EVENT_SOURCE": "com.swn.basket.checkoutbasket",
    "EVENT_DETAIL_TYPE": "CheckoutBasket",
    "EVENT_BUS_NAME": "SwnEventBus"
})
@mock_dynamodb
@mock_events
def test_lambda_handler_get_all_baskets(
    lambda_context
):
    from ...basket import lambda_handler
    # Initialize the DynamoDB table
    dynamo_db = boto3.resource("dynamodb")
    table = dynamo_db.create_table(
        TableName="basket",
        KeySchema=[{"AttributeName": "userName", "KeyType": "HASH"}],
        AttributeDefinitions=[{"AttributeName": "userName", "AttributeType": "S"}],
        BillingMode="PAY_PER_REQUEST"
    )
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
    "DYNAMODB_TABLE_NAME": "basket",
    "EVENT_SOURCE": "com.swn.basket.checkoutbasket",
    "EVENT_DETAIL_TYPE": "CheckoutBasket",
    "EVENT_BUS_NAME": "SwnEventBus"
})
@mock_dynamodb
@mock_events
def test_lambda_handler_get_basket_by_username(
    lambda_context
):
    from ...basket import lambda_handler
    # Initialize the DynamoDB table
    dynamo_db = boto3.resource("dynamodb")
    table = dynamo_db.create_table(
        TableName="basket",
        KeySchema=[{"AttributeName": "userName", "KeyType": "HASH"}],
        AttributeDefinitions=[{"AttributeName": "userName", "AttributeType": "S"}],
        BillingMode="PAY_PER_REQUEST"
    )
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

    event = {
        "httpMethod": "GET",
        "pathParameters": {
            "userName": "test_user"
        }
    }
    # Invoke the Lambda function
    response = lambda_handler(event, lambda_context)

    # Verify the response
    assert response["statusCode"] == 200
    res = json.loads(response["body"])

    assert "items" in res["body"]
    print(res["body"]["items"])
    assert res["body"]["items"] == item["items"]
    assert res["body"]["userName"] == item["userName"]

    # Clean up
    table.delete()


@mock.patch.dict('os.environ', {
    "DYNAMODB_TABLE_NAME": "basket",
    "EVENT_SOURCE": "com.swn.basket.checkoutbasket",
    "EVENT_DETAIL_TYPE": "CheckoutBasket",
    "EVENT_BUS_NAME": "SwnEventBus"
})
@mock_dynamodb
@mock_events
def test_lambda_handler_post_basket(
    lambda_context
):
    from ...basket import lambda_handler
    # Initialize the DynamoDB table
    dynamo_db = boto3.resource("dynamodb")
    table = dynamo_db.create_table(
        TableName="basket",
        KeySchema=[{"AttributeName": "userName", "KeyType": "HASH"}],
        AttributeDefinitions=[{"AttributeName": "userName", "AttributeType": "S"}],
        BillingMode="PAY_PER_REQUEST"
    )
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

    event = {
        "httpMethod": "POST",
        "path": "/basket",
        "body": json.dumps(item)
    }
    # Invoke the Lambda function
    response = lambda_handler(event, lambda_context)

    # Verify the response
    assert response["statusCode"] == 200

    # Clean up
    table.delete()


@mock.patch.dict('os.environ', {
    "DYNAMODB_TABLE_NAME": "basket",
    "EVENT_SOURCE": "com.swn.basket.checkoutbasket",
    "EVENT_DETAIL_TYPE": "CheckoutBasket",
    "EVENT_BUS_NAME": "SwnEventBus"
})
@mock_dynamodb
@mock_events
def test_lambda_handler_post_basket_checkout(
    lambda_context
):
    from ...basket import lambda_handler
    # Initialize the DynamoDB table
    dynamo_db = boto3.resource("dynamodb")
    event_bus = boto3.client("events")
    event_bus.create_event_bus(
        Name='SwnEventBus',
    )
    table = dynamo_db.create_table(
        TableName="basket",
        KeySchema=[{"AttributeName": "userName", "KeyType": "HASH"}],
        AttributeDefinitions=[{"AttributeName": "userName", "AttributeType": "S"}],
        BillingMode="PAY_PER_REQUEST"
    )
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

    event = {
        "httpMethod": "POST",
        "path": "/basket/checkout",
        "body": json.dumps(body)
    }
    # Invoke the Lambda function
    response = lambda_handler(event, lambda_context)

    # Verify the response
    assert response["statusCode"] == 200

    # Clean up
    table.delete()


@mock.patch.dict('os.environ', {
    "DYNAMODB_TABLE_NAME": "basket",
    "EVENT_SOURCE": "com.swn.basket.checkoutbasket",
    "EVENT_DETAIL_TYPE": "CheckoutBasket",
    "EVENT_BUS_NAME": "SwnEventBus"
})
@mock_dynamodb
@mock_events
def test_lambda_handler_delete_basket(
    lambda_context
):
    from ...basket import lambda_handler
    # Initialize the DynamoDB table
    dynamo_db = boto3.resource("dynamodb")
    table = dynamo_db.create_table(
        TableName="basket",
        KeySchema=[{"AttributeName": "userName", "KeyType": "HASH"}],
        AttributeDefinitions=[{"AttributeName": "userName", "AttributeType": "S"}],
        BillingMode="PAY_PER_REQUEST"
    )
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
    event = {
        "httpMethod": "DELETE",
        "path": "/basket",
        "pathParameters": {
            "userName": "test_user"
        }
    }
    # Invoke the Lambda function
    response = lambda_handler(event, lambda_context)

    # Verify the response
    assert response["statusCode"] == 200

    # Clean up
    table.delete()


@mock.patch.dict('os.environ', {
    "DYNAMODB_TABLE_NAME": "basket",
    "EVENT_SOURCE": "com.swn.basket.checkoutbasket",
    "EVENT_DETAIL_TYPE": "CheckoutBasket",
    "EVENT_BUS_NAME": "SwnEventBus"
})
@mock_dynamodb
@mock_events
def test_lambda_handler_wrong_route(
    lambda_context
):
    from ...basket import lambda_handler
    # Initialize the DynamoDB table
    dynamo_db = boto3.resource("dynamodb")
    table = dynamo_db.create_table(
        TableName="basket",
        KeySchema=[{"AttributeName": "userName", "KeyType": "HASH"}],
        AttributeDefinitions=[{"AttributeName": "userName", "AttributeType": "S"}],
        BillingMode="PAY_PER_REQUEST"
    )

    event = {
        "httpMethod": "PATCH",
        "path": "/basket",
    }
    # Invoke the Lambda function
    response = lambda_handler(event, lambda_context)

    # Verify the response
    assert response["statusCode"] == 400

    # Clean up
    table.delete()
