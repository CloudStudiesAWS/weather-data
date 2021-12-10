import time
import boto3
import json
from datetime import datetime


DATABASE = 'weather'
TABLE = 'weather_data'


bucket = 'cloud-studies-aws-artifacts'
keyQuery = 'root/artifacts/aws/query_scripts/hottest_day.sql'
keyView = 'root/artifacts/aws/query_views_ddl/view_hottest_day.sql'
_output='s3://cloud-studies-aws-analytics/output/hottest_day/execution_date=' + str(datetime.now().strftime("%d-%m-%Y"))


def lambda_handler(event, context):
    s3 = boto3.resource('s3')

    obj = s3.Object(bucket, keyQuery)
    
    query = obj.get()['Body'].read().decode('utf-8')

    clientAthena = boto3.client('athena')
    clientS3 = boto3.client('s3')

    # checking if there is older data on this day
    response = clientS3.list_objects(
        Bucket='cloud-studies-aws-analytics',
        Prefix='output/hottest_day/execution_date=' + str(datetime.now().strftime("%d-%m-%Y"))
    )

    # deleting any older data to replace with new one
    if response.get('Contents') is not None:
        for o in response['Contents']:
            responseDel = clientS3.delete_objects(
                Bucket='cloud-studies-aws-analytics',
                Delete={
                    'Objects': [
                        {
                            'Key': o.get('Key')
                        },
                    ],
                }
            )

    
    
    # Query create or replace View
    responseAthena = clientAthena.start_query_execution(
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
    response = clientAthena.start_query_execution(
        QueryString=query,
        QueryExecutionContext={
            'Database': DATABASE
        }
    )

    return {
        'statusCode': 200,
        'body': json.dumps(responseAthena)
    }
