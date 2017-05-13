# -*- coding: utf-8 -*-
import boto3
from botocore.exceptions import ClientError

def handler(event, context):
  try:
    table = boto3.resource('dynamodb', region_name='us-west-1').Table('menu')
    item = table.get_item(Key={'menu_id': event['menu_id']}).get('Item')
    if item == None:
      response = {}
      response['Message'] = 'Menu does not exist. Update failed'
      return response
    table.update_item(
      Key={'menu_id': event['menu_id']},
      UpdateExpression="SET selection = :a",
      ExpressionAttributeValues={':a': event['selection']}
      )
    response = {}
    return response
  except Exception as e:
    return e.message
