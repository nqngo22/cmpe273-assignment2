# -*- coding: utf-8 -*-
import boto3
import json
import time
from botocore.exceptions import ClientError

def handler(event, context):
  keys = {'input'}
  #Make sure the API is correct
  if all(key in event for key in keys):
    response = {}
    try:
      order_table = boto3.resource('dynamodb', region_name='us-west-1').Table('order')
      menu_table = boto3.resource('dynamodb', region_name='us-west-1').Table('menu')
    except Exception as e:
      #response[
      return e.message

    item = order_table.get_item(Key={'order_id': event['order_id']}).get('Item')
    #Get the customer's order
    order = item.get('order')
    menu_id = item.get('menu_id')
    #Get the customer's selection from the order
    if order.get('selection') == 'empty':
      #If the customer has not selected a selection, then update the table with the selection
      selection = menu_table.get_item(Key={'menu_id': menu_id}).get('Item').get('selection')[int(event.get('input'))-1]
      order['selection'] = selection
      sizes = menu_table.get_item(Key={'menu_id': menu_id}).get('Item').get('size')
      for i in range(0, len(sizes)):
        sizes[i] = str(i+1) +". " + sizes[i]
      sizes_str = ", ".join(sizes)
      response['Message'] = 'Which size do you want? ' + sizes_str
    elif order.get('size') == 'empty':
      #If the customer has not selected a size, then update the table with the size
      size = menu_table.get_item(Key={'menu_id': menu_id}).get('Item').get('size')[int(event.get('input'))-1]
      order['size'] = size
      cost = menu_table.get_item(Key={'menu_id': menu_id}).get('Item').get('price')[int(event.get('input'))-1]
      order['cost'] = cost
      response['Message'] = 'Your order costs $' + cost + '. We will email you when the order is ready. Thank you!'
      order['order_time'] = time.strftime("%m-%d-%Y@%H:%M:%S")
    else:
      return 
    order_table.update_item(
      Key={'order_id': event['order_id']},
      UpdateExpression="SET #order = :ss",
      ExpressionAttributeNames={'#order': 'order'},
      ExpressionAttributeValues={':ss': order}
    )
    #response['statusCode'] = 200
    #return json.dumps(response)
    return response
    
  else:
    return "missing keys"
