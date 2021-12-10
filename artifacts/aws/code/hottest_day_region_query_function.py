import time
import boto3
import json
from datetime import datetime


DATABASE = 'weather'
TABLE = 'weather_data'


bucket = 'cloud-studies-aws-artifacts'
keyQuery = 'root/artifacts/aws/query_scripts/hottest_day_region.sql'
keyView = 'root/artifacts/aws/query_views_ddl/view_hottest_day_region.sql'
_output='s3://cloud-studies-aws-analytics/output/hottest_day_region/execution_date='+ str(datetime.now().strftime("%d-%m-%Y"))


def lambda_handler(event, context):
    s3 = boto3.resource('s3')

    obj = s3.Object(bucket, keyQuery)
    
    query = obj.get()['Body'].read().decode('utf-8')

    client = boto3.client('athena')
    
    # Athena Query execution 
    response = client.start_query_execution(
        QueryString=query,
        QueryExecutionContext={
            'Database': DATABASE
        },
        ResultConfiguration={
            'OutputLocation': _output,
        }
    )

    obj = s3.Object(bucket, keyView)
    
    query = obj.get()['Body'].read().decode('utf-8')
    
    # Query create View
    response = client.start_query_execution(
        QueryString=query,
        QueryExecutionContext={
            'Database': DATABASE
        },
        ResultConfiguration={
            'OutputLocation': _output,
        }
    )

    return {
        'statusCode': 200,
        'body': json.dumps(response)
    }
