-- Which date was the hottest day?
select
    observation_date as hottest_day
from
    "weather"."weather_data"
where
    screen_temperature in (
        select
            max(screen_temperature)
        from
            "weather"."weather_data"
    )