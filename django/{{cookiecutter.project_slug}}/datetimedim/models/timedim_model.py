import datetime

import dateutil
from django.db import models

from datetimedim.models.managers import TimeDimManager


class TimeDim(models.Model):
    """
    The Time Dimension

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
    """

    # Fields
    time_actual = models.TimeField(unique=True)
    hour = models.PositiveSmallIntegerField()
    hour_str = models.CharField(max_length=2)
    hour_12 = models.PositiveSmallIntegerField()
    hour_12_str = models.CharField(max_length=2)
    minute = models.PositiveSmallIntegerField()
    minute_str = models.CharField(max_length=2)
    minute_of_day = models.PositiveSmallIntegerField()
    am_pm = models.CharField(max_length=2)

    objects = TimeDimManager()

    class Meta:
        ordering = ('minute_of_day',)

    def __str__(self):
        return f'{self.hour_str}:{self.minute_str} {self.am_pm}'

    def __sub__(self, minutes: int):
        """
        Subtracts minutes from TimeDim, returns another TimeDim. Midnight safe
        :param minutes:
        :return:
        """
        diff = self.minute_of_day - minutes
        return TimeDim.objects.fetch(diff)

    def __add__(self, minutes: int):
        """
        Adds minutes from TimeDim, returns another TimeDim. Midnight safe
        :param minutes:
        :return:
        """
        diff = self.minute_of_day + minutes
        return TimeDim.objects.fetch(diff)

    def __gt__(self, other):
        """
        Checks if self is greater than other TimeDim
        :param other:
        :return:
        """
        return self.minute_of_day > other.minute_of_day

    def __ge__(self, other):
        """
        Checks if self is greater than or equal to other TimeDim
        :param other:
        :return:
        """
        return self.minute_of_day >= other.minute_of_day

    def __lt__(self, other):
        """
        Checks if self is less than other TimeDim
        :param other:
        :return:
        """
        return self.minute_of_day < other.minute_of_day

    def __le__(self, other):
        """
        Checks if self is less than or equal other TimeDim
        :param other:
        :return:
        """
        return self.minute_of_day <= other.minute_of_day

    def tz_aware(self, date: datetime.date, tz='UTC'):
        tzinfo = dateutil.tz.gettz(tz)
        dt = datetime.datetime(year=date.year, month=date.month, day=date.day, hour=self.hour, minute=self.minute,
                               tzinfo=tzinfo)
        return dt

    def tz_aware_12_str(self, date: datetime.date, fmt='%I:%M %p %Z %z', tz='UTC'):
        return self.tz_aware(date, tz).strftime(fmt)

    def tz_aware_str(self, date: datetime.date, fmt='%H:%M %Z %z', tz='UTC'):
        return self.tz_aware(date, tz).strftime(fmt)

    def as_12(self):
        return f'{self.hour_12_str}:{self.minute_str} {self.am_pm}'

    def is_between(self, earlier, later, inclusive: bool = True) -> bool:
        """
        Checks if self is between earlier: TimeDim and later: TimeDim
        :param earlier: TimeDim
        :param later: TimeDim
        :param inclusive: bool
        :return: bool
        """

        if inclusive:
            return earlier <= self <= later
        return earlier < self < later
