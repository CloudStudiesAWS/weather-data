# weather-data
--- 
<p>This project goal is to:<br>
Convert the weather data into parquet format. Set the row group to the appropriate value you see fit for this data.</p>

The converted data should be able to answer the following question: 
 - Which date was the hottest day?
 - What was the temperature on that day?
 - In which region was the hottest day?
 ---
 The solution is hibrid, having a bash script to sync local data and code with AWS S3 bucket.
 We need to have AWS CLI installed and configured the the local machine.
 https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-getting-started.html


---

Role added to run lambda

---

Policy created AthenaQueryGroup

---

Bucket structure 
 - raw -> Analytics

---

Assumption about the data:
 - The screen_temperature field is used to measure the temperature about the observed day(observation_date)
 
 > S3 Select feature can be used to see query results csv
  - s3://cloud-studies-aws-analytics/output/*

--- 
Lambda funcction to process the weather data
 - Increased the lambda function memory and execution time to process the data using awswrangler and pandas

 