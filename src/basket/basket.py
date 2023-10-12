import json
from os import environ

import boto3

dynamo_db_resource = boto3.resource('dynamodb')
event_bridge = boto3.client('events')
dynamo_db_table_name = environ["DYNAMODB_TABLE_NAME"]
table = dynamo_db_resource.Table(dynamo_db_table_name)


def lambda_handler(event, context):
    try:
        http_method = event['httpMethod']
        body = None

        if http_method == "GET":
            if event.get('pathParameters'):
                body = get_basket(event['pathParameters']['userName'])
            else:
                body = get_all_baskets()
        elif http_method == "POST":
            if event['path'] == "/basket/checkout":
                body = checkout_basket(event)
            else:
                body = create_basket(event)
        elif http_method == "DELETE":
            body = delete_basket(event['pathParameters']['userName'])
        else:
            return {
                'statusCode': 400,
                'body': json.dumps({
                    'message': f"Unsupported route: {http_method}",
                })
            }

        print(body)
        return {
            'statusCode': 200,
            'body': json.dumps({
                'message': f'Successfully finished operation: "{http_method}"',
                'body': body
            }, default=str)
        }
    except Exception as e:
        print(e)
        return {
            'statusCode': 500,
            'body': json.dumps({
                'message': 'Failed to perform operation.',
                'errorMsg': str(e),
            }, default=str)
        }


def get_basket(user_name):
    try:
        response = table.get_item(
            Key={'userName': user_name}
        )
        item = response.get('Item')
        return item if item else {}
    except Exception as e:
        print(e)
        raise e


def get_all_baskets():
    try:
        response = table.scan()
        items = response.get('Items', [])
        return items
    except Exception as e:
        print(e)
        raise e


def create_basket(event):
    try:
        request_body = json.loads(event['body'])
        print(request_body)
        table.put_item(
            Item=request_body
        )
        return {}
    except Exception as e:
        print(e)
        raise e


def delete_basket(user_name):
    try:
        table.delete_item(
            Key={'userName': user_name}
        )
        return {}
    except Exception as e:
        print(e)
        raise e


def checkout_basket(event):
    try:
        checkout_request = json.loads(event['body'])
        user_name = checkout_request.get('userName')
        if not user_name:
            raise Exception("userName should exist in checkoutRequest")

        basket = get_basket(user_name)
        checkout_payload = prepare_order_payload(checkout_request, basket)
        publish_checkout_basket_event(checkout_payload)
        delete_basket(user_name)
        return {}
    except Exception as e:
        print(e)
        raise e


def prepare_order_payload(checkout_request, basket):
    try:
        if not basket or 'items' not in basket:
            raise Exception("basket should exist in items")

        total_price = sum(float(item['price']) for item in basket.get('items', []))
        checkout_request['totalPrice'] = str(total_price)
        checkout_request.update(basket)
        return checkout_request
    except Exception as e:
        print(e)
        raise e


def publish_checkout_basket_event(checkout_payload):
    print("publish_checkout_basket_event")
    try:
        event_payload = json.dumps(checkout_payload, default=str)

        event_source = environ["EVENT_SOURCE"]
        detail_type = environ["EVENT_DETAIL_TYPE"]
        event_bus_name = environ["EVENT_BUS_NAME"]
        entry = {
                'Source': event_source,
                'Detail': event_payload,
                'DetailType': detail_type,
                'EventBusName': event_bus_name
            }
        print(entry)
        event_bridge.put_events(
            Entries=[entry]
        )
    except Exception as e:
        print(e)
        raise e
