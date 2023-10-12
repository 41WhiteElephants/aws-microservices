import json
from decimal import Decimal
import boto3
import uuid
from os import environ

dynamo_db_resource = boto3.resource('dynamodb')
dynamo_db_table_name = environ["DYNAMODB_TABLE_NAME"]


def lambda_handler(event, context):
    print("request:", json.dumps(event, indent=2))

    try:
        http_method = event['httpMethod']
        body = None

        if http_method == "GET":
            if event.get('queryStringParameters'):
                body = get_products_by_category(event)
            elif event.get('pathParameters'):
                body = get_product(event['pathParameters']['id'])
            else:
                body = get_all_products()
        elif http_method == "POST":
            body = create_product(event)
        elif http_method == "DELETE":
            body = delete_product(event['pathParameters']['id'])
        elif http_method == "PUT":
            body = update_product(event)
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
            })
        }

    except Exception as e:
        print(e)
        return {
            'statusCode': 500,
            'body': json.dumps({
                'message': 'Failed to perform operation.',
                'errorMsg': str(e),
            })
        }


def get_product(product_id):
    print("get_product")

    try:
        table = dynamo_db_resource.Table(dynamo_db_table_name)
        response = table.get_item(Key={'id': product_id})
        item = response.get('Item')
        return item or {}

    except Exception as e:
        print(e)
        raise e


def get_all_products():
    print("get_all_products")

    try:
        table = dynamo_db_resource.Table(dynamo_db_table_name)
        response = table.scan()
        items = response.get('Items', [])
        return items

    except Exception as e:
        print(e)
        raise e


def create_product(event):
    print(f"create_product function. event : {event}")

    try:
        product_request = json.loads(event['body'])
        product_id = str(uuid.uuid4())
        # dynamodb accepts Decimal or str so it's handy
        # to keep prices as strings ( no redundant Decimal -> float conversions when retrieving data from db)
        # from the other hand it's ok to have strings for price displaying but for math operations it should
        # be converted to floats
        # todo: think of changing prices and item counts to numbers instead of strings
        product_request['id'] = product_id

        table = dynamo_db_resource.Table(dynamo_db_table_name)
        response = table.put_item(Item=product_request)
        print(response)
        return response

    except Exception as e:
        print(e)
        raise e


def delete_product(product_id):
    print(f"delete_product function. product_id : {product_id}")

    try:
        table = dynamo_db_resource.Table(dynamo_db_table_name)
        response = table.delete_item(Key={'id': product_id})
        print(response)
        return response

    except Exception as e:
        print(e)
        raise e


def update_product(event):
    print(f"update_product function. event : {event}")

    try:
        request_body = json.loads(event['body'])
        obj_keys = list(request_body.keys())

        table = dynamo_db_resource.Table(dynamo_db_table_name)
        update_expression = "SET " + ", ".join([f"#key{i} = :value{i}" for i in range(len(obj_keys))])
        expression_attribute_names = {f"#key{i}": key for i, key in enumerate(obj_keys)}
        expression_attribute_values = {f":value{i}": value for i, (key, value) in enumerate(request_body.items())}

        response = table.update_item(
            Key={'id': event['pathParameters']['id']},
            UpdateExpression=update_expression,
            ExpressionAttributeNames=expression_attribute_names,
            ExpressionAttributeValues=expression_attribute_values
        )
        print(response)
        return response

    except Exception as e:
        print(e)
        raise e


def get_products_by_category(event):
    print("get_products_by_category")

    try:
        product_id = event['pathParameters']['id']
        category = event['queryStringParameters']['category']

        table = dynamo_db_resource.Table(dynamo_db_table_name)
        response = table.query(
            KeyConditionExpression='id = :product_id',
            FilterExpression='contains (category, :category)',
            ExpressionAttributeValues={':product_id': product_id, ':category': category}
        )
        items = response.get('Items', [])
        return items

    except Exception as e:
        print(e)
        raise e
