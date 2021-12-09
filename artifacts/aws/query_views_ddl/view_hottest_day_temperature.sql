-- View Example
CREATE OR REPLACE VIEW hottest_day_temperature AS
-- What was the temperature on that day?
select
    max(screen_temperature) as hottest_day_temperature
from
    "weather"."weather_data";