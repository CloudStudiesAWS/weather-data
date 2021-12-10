# weather-data
--- 
<p>This project goal is to:<br>
Convert the weather data into parquet format. Set the row group to the appropriate value you see fit for this data.</p>

The converted data should be able to answer the following question: 
 - Which date was the hottest day?
 - What was the temperature on that day?
 - In which region was the hottest day?
 ---
 The solution is hibrid, having bash script to sync local data and code with AWS S3 bucket.
 We need to have AWS CLI installed and configured at the local machine.
 https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-getting-started.html

---

Assumption about the data and considerations:
 - The screen_temperature field is used to measure the temperature about the observed day(observation_date)
 - Lambda function to process the weather data
    - Increased the lambda function memory and execution time to process the data using awswrangler and pandas

--- 
 
<h3>Solution Explanation</h3>

--- 

<p>This is the project repository that I use to do the challenge: https://github.com/CloudStudiesAWS/weather-data</p>
<p>A quick video demonstration was made to ilustrate the data pipeline: https://youtu.be/x42Eqy38Uic </p>

> To execute the pipeline and get the awnsers, an *AWS CLI must be configured* and the User must have S3 permissions.


> In the C:\Users\PICHAU\dev\weather-data\artifacts\local\ folder I create 2 .bat file to run an AWS s3 sync command: 
 - sync-code.bat -> Send all new and updated arctifacts to s3 *cloud-studies-aws-artifacts* bucket
 - sync-data.bat -> Send all new and updated data to s3 *cloud-studies-aws-raw bucket*

> First of all, I need to run the *sync-code.bat* file to upload some script that I'm going to use on Lambda Functions to get the final results and create views to get those results usign Athena.

> Then I just need to run the second *sync-data.bat* file to upload the weather data to the raw bucket.

> Once the data lands to cloud-studies-aws-raw bucket, the data pipeline flow starts.
The data arrives to the *csv_data/* folder, where a rule is configured to trigger a lambda function named *data-process-function* that is going to process this csv data using *awswrangler*, create a database and table if needed, organize this data on partitions and write it as parquet in another bucket named *cloud-studies-aws-analytics*.

> At the end of this lambda function 3 message are sent to SQS queues. Those SQS are used as trigger to another 3 lambda functions named hottest_day_query_function, hottest_day_region_query_function, hottest_day_temperature_query_function.

> Each function are going to load a sql script that the first .bat file uploaded to the arctifact bucket and it will use those sql scripts to awnser the questions.

> Those lambdas functions will use the Athena client to query the weather database that awswrangler have created and the query result is going to be saved at the cloud-studies-aws-analytics bucket, using the following structure: 
- output: 
> - hottest_day_region/dd-mm-yyyy/result_csv_with_randon_name.csv
> - hottest_day_temperature/dd-mm-yyyy/result_csv_with_randon_name.csv
> - hottest_day/dd-mm-yyyy/result_csv_with_randon_name.csv

> This way, if the data uploaded is on a monthly basis as it suggest, every first day of the month the new data is going to be stored as shown.

> Also, if anyone wants to query data ad-hoc, the database is available on Athena and each the query used to get the final results are created as Athena Views, so if anyone want to check the result using using the AWS console, there is 2 very easy ways:
 - First, quering the Athena views hottest_day, hottest_day_region and hottest_day_temperature
	- Sample: SELECT * FROM "weather"."hottest_day" (return only one record, so it is not a problem to use select * without where)
 - Second: Using S3 Select
   - At Amazon S3, Check the sample file: cloud-studies-aws-analytics/output/hottest_day_region/09-12-2021/6f74ab1e-2b31-4781-a83d-cc63c5adc676.csv and select Actions> Query with S3 Select and execute a simple query to see the record on it

*NOTE: The first execution when both csv files is uploaded at same time to s3, the output result is duplicated (same right result). The followings executions will delete old data and retain only one csv file result até the analytics output bucket. 

> That is all, I hope you enjoy it, I have a lot of fun building this, thank you! :D

--- 

<h1>Images</h1>

--- 

## Query to valida the rightness of the hottest day
![Validating the hottest day](/artifacts/images/validate_hottest_day.png)

## Hottest day query result 
![Athena Results](/artifacts/images/hottest_day_result.png)

--- 

## The raw bucket final structure
![Bucket Structure](/artifacts/images/raw_bucket_structure.png)

---

## The sync command executed

![Sync code command](/artifacts/images/sync_code.png)

---

## Views with the results
![Athena View Results](/artifacts/images/athena_view_results.png)

--- 
