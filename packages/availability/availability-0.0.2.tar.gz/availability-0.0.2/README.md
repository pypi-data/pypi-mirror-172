# Availability
Python type for working with ranges of datetimes


Use Availability to calculate ranges of datetimes.  A range consists of a start and end time that can be added or subtracted from another range.

```
availability = Availabilty([
AvailabilityRange(start_time=datetime.datetime(2022,11,1), end_time=datetime.datetime(2022,11,31,23,59,59)),
], padding_time_before=5, padding_time_after=10)

availability -= AvailabilityRange(start_time=datetime.datetime(2022,11,8), end_time=datetime.datetime(2022,11,10))
```
