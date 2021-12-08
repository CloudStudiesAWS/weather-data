import time
import boto3
import json


DATABASE = 'weather'
TABLE = 'weather_data'

output='s3://cloud-studies-aws-raw/query_result/result-query-triggered/'


def lambda_handler(event, context):


    # query = "SELECT * FROM %s.%s where %s = '%s';" % (DATABASE, TABLE, COLUMN, keyword)
    query = "SELECT * FROM %s.%s;" %(DATABASE, TABLE)
    client = boto3.client('athena')

    # Execution
    response = client.start_query_execution(
        QueryString=query,
        QueryExecutionContext={
            'Database': DATABASE
        },
        ResultConfiguration={
            'OutputLocation': output,
        }
    )


    return {
        'statusCode': 200,
        'body': json.dumps(response)
    }
