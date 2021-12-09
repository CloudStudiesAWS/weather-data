-- What was the temperature on that day?
select
    max(screen_temperature) as hottest_day_temperature
from
    "weather"."weather_data"