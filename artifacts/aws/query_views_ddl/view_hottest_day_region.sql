-- View Example
CREATE OR REPLACE VIEW hottest_day_region AS
-- In which region was the hottest day?
select
    region as hottest_day_region
from
    "weather"."weather_data"
where
    screen_temperature in (
        select
            max(screen_temperature)
        from
            "weather"."weather_data"
    );