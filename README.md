# weather-data
--- 
<p>This project goal is to:<br>
Convert the weather data into parquet format. Set the row group to the appropriate value you see fit for this data.</p>

The converted data should be able to answer the following question: 
 - Which date was the hottest day?
 - What was the temperature on that day?
 - In which region was the hottest day?
 ---
 The solution is hibrid, having a bash script to sync local data with AWS S3.
 We need to have AWS CLI installed and configured the the local machine.
 https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-getting-started.html

--- 
 