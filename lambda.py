import json
import boto3
from decimal import Decimal

def lambda_handler(event, context):
    
    time = event["time"]
    tempC = event['temp']
    tempk = tempC + 273.15
    reponse = insertBD(time,tempC,tempk) 
    print(reponse)
    
    
def insertBD(timestamp, tempC, tempk):
        dynamodb = boto3.resource('dynamodb',region_name = "us-west-2")
        table = dynamodb.Table('TestDB')
        responce = table.put_item(
        Item = {
            'TimeStamp': timestamp,
            'TempCelsius': str(tempC),
            'TempKelvin': str(tempk)}
            )
        return responce