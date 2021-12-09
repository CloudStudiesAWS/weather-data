import time
import boto3
import json
from datetime import datetime


DATABASE = 'weather'
TABLE = 'weather_data'

_input='s3://cloud-studies-aws-artifacts/root/artifacts/aws/query_scripts/hottest_day.sql'
bucket = 'cloud-studies-aws-artifacts'
key = 'root/artifacts/aws/query_scripts/hottest_day.sql'
_output='s3://cloud-studies-aws-analytics/output/hottest_day/execution_date=' + str(datetime.now().strftime("%d-%m-%Y"))


def lambda_handler(event, context):
    s3 = boto3.resource('s3')

    obj = s3.Object(bucket, key)
    
    query = obj.get()['Body'].read().decode('utf-8')
    print(query)

    client = boto3.client('athena')
    
    # Athena Execution
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
