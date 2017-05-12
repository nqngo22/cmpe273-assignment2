# -*- coding: utf-8 -*-
import boto3
from botocore.exceptions import ClientError

def handler(event, context):
  try:
    table = boto3.resource('dynamodb', region_name='us-west-1').Table('menu')
    table.put_item(Item=event)
  except Exception as e:
    return e.message
