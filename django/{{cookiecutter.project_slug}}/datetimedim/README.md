# Django DateTimeDimesion

Django DateTimeDimesion is a droppable Django app for dealing with dates and times as dimension tables.

## Status: 0.0.3
TODO:
- Date Dimension
    - [x] Overload +, -, /, //, >, >=, <, <= operators
    - [ ] Seasons
    - [ ] Fiscal schedules
    - [ ] Performance tuneups for range selections
- Time Dimension
    - [x] Model
        - [x] Define methods
        - [x] Overload +, -, >, >=, <, <= operators
    - [x] Manager
        - [x] Define methods
    - [ ] Sunrise/sunset
    - [ ] Time of day descriptors

```pydocstring
DateDim object
Fields:
        date_actual (datetime.date)         : Actual date object
        day (int)                           :
        day_abbr (str)                      :
        day_name (str)                      :
        day_of_month (int)                  :
        day_of_quarter (int)                :
        day_of_week (int)                   :
        day_of_year (int)                   :
        day_str (str)                       : Zero-padded day number
        epoch (int)                         : Number of days since January 1, 0001
        first_day_of_month (datetime.date)  :
        first_day_of_quarter (datetime.date):
        first_day_of_week (datetime.date)   :
        first_day_of_year (datetime.date)   :
        is_weekend (bool)                   :
        last_day_of_month (datetime.date)   :
        last_day_of_quarter (datetime.date) :
        last_day_of_week (datetime.date)    :
        last_day_of_year (datetime.date)    :
        month (int)                         :
        month_abbr (str)                    :
        month_name (str)                    :
        month_str (str)                     : Zero-padded month number
        quarter (int)                       :
        quarter_name (str)                  :
        week_date_iso (int)                 :
        week_iso (int)                      :
        week_of_month (int)                 :
        week_of_year (int)                  :
        year (int)                          :
        year_actual_iso (int)               :
        nicename_long (str)                 : Tuesday, January 5, 1993
        nicename_short (str)                : Tue, Jan 5, 1993

    Methods:
        __str__() -> str                                : Returns isoformat
        as_arrow() -> arrow.arrow.Arrow                 : Returns self as an arrow object
        tomorrow() -> DateDim                           :
        yesterday() -> DateDim                          :
        next_week() -> DateDim                          :
        last_week() -> DateDim                          :
        next_month() -> DateDim                         :
        last_month() -> DateDim                         :
        is_between(earlier, later, inclusive) -> bool   : Returns true if self is between earlier and later
    
    Overloaded operators:
        DateDim > DateDim                               : Greater Than -> bool
        DateDim >= DateDim                              : Greater Than or Equal To -> bool
        DateDim < DateDim                               : Less Than -> bool
        DateDim <= DateDim                              : Less Than or Equal To -> bool
        DateDim + int                                   : DateDim plus days -> DateDim
        DateDim - int                                   : DateDim minus days -> DateDim
        DateDim / int                                   : DateDim divided by int segments -> List[TimeDim] (inclusive)
        DateDim // int                                  : DateDim divided by int segments -> List[TimeDim] (exclusive)

TimeDim object
    Fields:
        time_actual (datetime.time)                     :
        hour (int)                                      :
        hour_str (str)                                  :
        hour_12 (int)                                   :
        hour_12_str (str)                               :
        minute (int)                                    :
        minute_str (str)                                :
        minute_of_day (int)                             : Minutes since midnight
        am_pm (str)                                     : AM or PM

    Methods:
        __str__() -> str                                : Returns HH:MM P (military time)
        as_12() -> str                                  : Returns HH:MM P (12-hour time)
        tz_aware(date, tz=UTC) -> datetime              : Returns a timezone aware datetime object
        is_between(earlier, later, inclusive) -> bool   : Returns true if self is between earlier and later
        
    Overloaded operators:
        TimeDim > TimeDim                               : Greater Than -> bool
        TimeDim >= TimeDim                              : Greater Than or Equal To -> bool
        TimeDim < TimeDim                               : Less Than -> bool
        TimeDim <= TimeDim                              : Less Than or Equal To -> bool
        TimeDim + int                                   : TimeDim plus days -> TimeDim
        TimeDim - int                                   : TimeDim minus days -> TimeDim
```

## Installation

`¯\_(ツ)_/¯`

Add to your `INSTALLED_APPS` in `settings.py`:
```python
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    ...
    'datetimedim',
    ...
]

```
Use as is, or extend.

## Usage
### Manager objects
- Populate entire years
```python
DateDim.objects.bootstrap(years=[2019, 2025], week_starts_on=1)
```
- Create a day
```python
DateDim.objects.create(year=2019, month=3, day=30)
```
- Fetch a day
```python
DateDim.objects.fetch('yyyy-mm-dd')
```
or
```python
DateDim.objects.fetch(datetime.date)
```
or
```python
DateDim.objects.fetch(datetime.datetime)
```
- Fetch date range
```python
DateDim.objects.fetch_range(start=datetime.date, end=datetime.date, day_of_week_include=[int], day_of_week_exclude=[int])
```
Note that this will fail if the date range falls on dates not previously created. If you want to be safe, add the `safe=True` parameter.
- Fetch all date dims in year
```python
DateDim.objects.year(2019)
```
- Fetch all date objects in month of specific year
```python
DateDim.objects.month(year=2019, month=3)
# method chaining:
DateDim.objects.year(2019).month(3)
```
- Fetch all date objects in week of a specific date dim
```python
day = DateDim.objects.fetch(datetime.date.today())
DateDim.objects.fetch_range(start=day.first_day_of_week, end=day.last_day_of_week)
```
- Chainable querysets
```python
DateDim.objects.year(2019).weekdays()
DateDim.objects.year(2019).weekends()
DateDim.objects.year(2019).month(1).weekdays()
# ... you get the idea

```

### Model object instances
```python
d = DateDim.objects.fetch(datetime.date.today())
# The following will return DateDim objects:
d.tomorrow()
d.yesterday()
d.next_week()
d.last_week()
d.next_month()
d.last_month()
d.next_week().last_month().tomorrow().last_week().yesterday() # Don't do this

d + 1 # same as d.tomorrow()
d + 1 + 1 # same as d.tomorrow().tomorrow()
d - 1 # same as d.yesterday()

d / 12 # splits d into 12 TimeDims, inclusive (ex: 0:00 to 1:00, 1:00 to 2:00...)
d // 12 # splits d into 12 TimeDims, exclusive (ex: 0:00 to 0:59, 1:00 to 1:59...)
```

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License
[MIT](https://choosealicense.com/licenses/mit/)
