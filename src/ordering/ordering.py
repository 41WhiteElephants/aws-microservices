from os import environ
import json
import boto3
from datetime import datetime
from botocore.exceptions import ClientError

dynamo_db_resource = boto3.resource('dynamodb')
dynamo_db_table_name = environ["DYNAMODB_TABLE_NAME"]
table = dynamo_db_resource.Table(dynamo_db_table_name)


def lambda_handler(event, context):
    print("request:", json.dumps(event, indent=2))

    if 'Records' in event:
        for record in event['Records']:
            sqs_invocation(record)
    elif 'detail-type' in event:
        event_bridge_invocation(event)
    else:
        return api_gateway_invocation(event)


def sqs_invocation(record):
    try:
        checkout_event_request = json.loads(record['body'])
        create_order(checkout_event_request['detail'])
    except Exception as e:
        print(e)
        raise e


def event_bridge_invocation(event):
    try:
        create_order(event['detail'])
    except Exception as e:
        print(e)
        raise e


def create_order(basket_checkout_event):
    try:
        order_date = datetime.utcnow().isoformat()

        item = {
                'userName': basket_checkout_event.pop('userName'),
                'orderDate': order_date,
                'data': basket_checkout_event
        }

        response = table.put_item(Item=item)
        return response

    except ClientError as e:
        print(e)
        raise e


def api_gateway_invocation(event):
    try:
        http_method = event['httpMethod']
        body = None

        if http_method == "GET":
            if event.get('pathParameters'):
                body = get_order(event)
            else:
                body = get_all_orders()
        else:
            return {
                'statusCode': 400,
                'body': json.dumps({
                    'message': f"Unsupported route: {http_method}",
                })
            }

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


def get_order(event):
    try:
        user_name = event['pathParameters']['userName']
        order_date = event['queryStringParameters']['orderDate']

        params = {
            'KeyConditionExpression': 'userName = :userName and orderDate = :orderDate',
            'ExpressionAttributeValues': {
                ':userName': user_name,
                ':orderDate': order_date
            }
        }

        response = table.query(**params)
        items = response.get('Items', [])
        # only 1 item match search for an order with a given user_name and order_date
        return items[0]

    except Exception as e:
        print(e)
        raise e


def get_all_orders():
    try:
        response = table.scan()
        items = response.get('Items', [])
        return items

    except Exception as e:
        print(e)
        raise e
