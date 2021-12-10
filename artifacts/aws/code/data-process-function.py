import json
import awswrangler as wr
import boto3
import pandas as pd
from datetime import datetime

s3 = boto3.resource('s3')

client = boto3.client('sns')

def lambda_handler(event, context):
    type(event)
    for record in event['Records']:

        # TODO implement
        key = record.get('s3').get('object').get('key')
        bucket = record.get('s3').get('bucket').get('name')
        
    
        # obj = s3.Object(bucket, key)
        data_path = f"s3://{bucket}/{key}"
        db_path = f"s3://{bucket}/weather/"
    
        
        df = wr.s3.read_csv(data_path)
        
        # creating the database if not exists 
        if "weather" not in wr.catalog.databases().values:
            wr.catalog.create_database("weather")
        
        
        # building table partition column 
        df['ObservationDate'] = pd.to_datetime(df['ObservationDate']).dt.date
    
        # 2016-02-01T00:00:00
        wr.s3.to_parquet(
            df=df,
            path=db_path,
            index=False,
            dataset=True,
            mode="overwrite_partitions",
            database="weather",
            table="weather_data",
            partition_cols=["ObservationDate"]
        )
        
    # SNS publish msg to start posteriors query executions
    response = client.publish(
        TargetArn='arn:aws:sns:us-east-1:004770887468:trigger-query-results',
        Message='Trigger lambdas to query data'
    )
            
            
    return {
        'statusCode': 200,
        'body': json.dumps(event)
    }
