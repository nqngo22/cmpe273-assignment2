# -*- coding: utf-8 -*-
import boto3
from botocore.exceptions import ClientError

def handler(event, context):
  try:
    table = boto3.resource('dynamodb', region_name='us-west-1').Table('menu')
    item = table.get_item(Key={'menu_id': event['menu_id']}).get('Item')
    return item
  except Exception as e:
    return e.message
