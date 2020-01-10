import arrow
from django.apps import apps
from django.db import models

from datetimedim.models.managers import DateDimManager


class DateDim(models.Model):
    """
    The Date Dimension

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
        as_arrow() -> arrow.arrow.Arrow     : Returns self as an arrow object
        tomorrow() -> DateDim
        yesterday() -> DateDim
        next_week() -> DateDim
        last_week() -> DateDim
        next_month() -> DateDim
        last_month() -> DateDim

    """

    # Fields
    day = models.PositiveSmallIntegerField()
    day_str = models.CharField(max_length=2)
    date_actual = models.DateField(unique=True)
    epoch = models.PositiveIntegerField(unique=True)
    day_name = models.CharField(max_length=9)
    day_abbr = models.CharField(max_length=3)
    day_of_week = models.PositiveSmallIntegerField()
    day_of_month = models.PositiveSmallIntegerField()
    day_of_quarter = models.PositiveSmallIntegerField()
    day_of_year = models.PositiveSmallIntegerField()
    week_of_month = models.PositiveSmallIntegerField()
    week_of_year = models.PositiveSmallIntegerField()
    month = models.PositiveSmallIntegerField()
    month_str = models.CharField(max_length=2)
    month_name = models.CharField(max_length=9)
    month_abbr = models.CharField(max_length=3)
    quarter = models.PositiveSmallIntegerField()
    quarter_name = models.CharField(max_length=9)
    year = models.PositiveSmallIntegerField()
    first_day_of_week = models.DateField()
    last_day_of_week = models.DateField()
    first_day_of_month = models.DateField()
    last_day_of_month = models.DateField()
    first_day_of_quarter = models.DateField()
    last_day_of_quarter = models.DateField()
    first_day_of_year = models.DateField()
    last_day_of_year = models.DateField()
    is_weekend = models.BooleanField(default=False)
    year_actual_iso = models.PositiveSmallIntegerField()
    week_iso = models.PositiveSmallIntegerField()
    week_date_iso = models.PositiveSmallIntegerField()
    nicename_long = models.CharField(max_length=64)
    nicename_short = models.CharField(max_length=32)

    objects = DateDimManager()

    class Meta:
        ordering = ('date_actual',)
        unique_together = ('day', 'month', 'year')

    def __str__(self):
        return self.date_actual.isoformat()

    def __sub__(self, days: int):
        """
        Subtracts days from DateDim, returns another DateDim
        :param days:
        :return:
        """
        return DateDim.objects.fetch(self.epoch - days)

    def __add__(self, days: int):
        """
        Adds days to DateDim, returns another DateDim
        :param days:
        :return:
        """
        return DateDim.objects.fetch(self.epoch + days)

    def __truediv__(self, sections: int):
        """
        Returns a list of QuerySets of TimeDim blocks divided by <sections>, inclusive
        :param sections:
        :return:
        """
        TimeDim = apps.get_model('datetimedim.TimeDim')
        span = 1440 // sections
        parts = [(i, i + span) for i in range(0, 1440, span)]
        divs = []
        for part in parts:
            divs.append(
                TimeDim.objects.filter(minute_of_day__gte=part[0], minute_of_day__lte=part[1]),
            )
        return divs

    def __floordiv__(self, sections: int):
        """
        Returns a list of QuerySets of TimeDim blocks divided by <sections>, exclusive
        :param sections:
        :return:
        """
        TimeDim = apps.get_model('datetimedim.TimeDim')
        span = 1440 // sections
        parts = [(i, i + span) for i in range(0, 1440, span)]
        divs = []
        for part in parts:
            divs.append(
                TimeDim.objects.filter(minute_of_day__gte=part[0], minute_of_day__lte=part[1] - 1),
            )
        return divs

    def __gt__(self, other):
        """
        Checks if self is greater than other DateDim
        :param other:
        :return:
        """
        return self.epoch > other.epoch

    def __ge__(self, other):
        """
        Checks if self is greater than or equal to other DateDim
        :param other:
        :return:
        """
        return self.epoch >= other.epoch

    def __lt__(self, other):
        """
        Checks if self is less than other DateDim
        :param other:
        :return:
        """
        return self.epoch < other.epoch

    def __le__(self, other):
        """
        Checks if self is less than or equal other DateDim
        :param other:
        :return:
        """
        return self.epoch <= other.epoch

    def as_arrow(self):
        """

        :return:
        """
        return arrow.get(self.date_actual)

    def tomorrow(self):
        """

        :return:
        """
        try:
            return DateDim.objects.get(epoch=self.epoch + 1)
        except DateDim.DoesNotExist:
            return DateDim.objects.fetch(self.as_arrow().shift(days=1).date())

    def yesterday(self):
        """

        :return:
        """
        try:
            return DateDim.objects.get(epoch=self.epoch - 1)
        except DateDim.DoesNotExist:
            return DateDim.objects.fetch(self.as_arrow().shift(days=-1).date())

    def next_week(self):
        """

        :return:
        """
        try:
            return DateDim.objects.get(epoch=self.epoch + 7)
        except DateDim.DoesNotExist:
            return DateDim.objects.fetch(self.as_arrow().shift(days=7).date())

    def last_week(self):
        """

        :return:
        """
        try:
            return DateDim.objects.get(epoch=self.epoch - 7)
        except DateDim.DoesNotExist:
            return DateDim.objects.fetch(self.as_arrow().shift(days=-7).date())

    def next_month(self):
        """

        :return:
        """
        try:
            return DateDim.objects.get(
                date_actual=self.as_arrow().shift(months=1).date()
            )
        except DateDim.DoesNotExist:
            return DateDim.objects.fetch(self.as_arrow().shift(months=1).date())

    def last_month(self):
        """

        :return:
        """
        try:
            return DateDim.objects.get(
                date_actual=self.as_arrow().shift(months=-1).date()
            )
        except DateDim.DoesNotExist:
            return DateDim.objects.fetch(self.as_arrow().shift(months=-1).date())

    def is_between(self, earlier, later, inclusive: bool = True) -> bool:
        """
        Checks if self is between earlier: DateDim and later: DateDim
        :param inclusive: bool
        :param earlier: DateDim
        :param later: DateDim
        :return: bool
        """
        if inclusive:
            return earlier <= self <= later
        return earlier < self < later
