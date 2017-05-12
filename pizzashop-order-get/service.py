# -*- coding: utf-8 -*-
import boto3
import json
from botocore.exceptions import ClientError

def handler(event, context):
  keys = {'order_id'}
  #Make sure the API is correct
  if all(key in event for key in keys):
    try:
      order_table = boto3.resource('dynamodb', region_name='us-west-1').Table('order')
    except Exception as e:
      return e.message

    item = order_table.get_item(Key={'order_id': event['order_id']}).get('Item')
    return item
    #return json.dumps(item)
    #your_json = '["foo", {"bar":["baz", null, 1.0, 2]}]'
    #parsed = json.loads(your_json)
    #return json.dumps(parsed, indent=4, sort_keys=True)
    #return json.dumps(parsed)

  else:
    return "missing key: order_id"
