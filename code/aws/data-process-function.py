import json
import awswrangler as wr
import boto3
import pandas as pd
from datetime import datetime


s3 = boto3.resource('s3')



def lambda_handler(event, context):
    # TODO implement
    for record in event['Records']:
        object = record.get('s3').get('object')
        bucket = record.get('s3').get('bucket').get('name')
        # {'key': 's3://cloud-studies-aws-raw/data/weather.20160201.csv', 'size': 1024, 'eTag': '0123456789abcdef0123456789abcdef', 'sequencer': '0A1B2C3D4E5F678901'}
        key = object.get('key')

        obj = s3.Object(bucket, key)
        data_path = f"s3://{bucket}/data/"
        db_path = f"s3://{bucket}/weather/"
        print(data_path)
        # obj.get()['Body'].read().decode('utf-8')
        # df = wr.s3.read_csv("s3://bucket/dataset/", dataset=True)
        # df = wr.s3.read_csv("s3://bucket/dataset/", dataset=True)
        df = wr.s3.read_csv(data_path)
        
        if "weather" not in wr.catalog.databases().values:
            wr.catalog.create_database("weather")
        
        df['ObservationDate'] = pd.to_datetime(df['ObservationDate']).dt.date

        print(df['ObservationDate'])
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
        
    wr.athena.read_sql_query("SELECT * FROM weather_data", database="weather")
    
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }
