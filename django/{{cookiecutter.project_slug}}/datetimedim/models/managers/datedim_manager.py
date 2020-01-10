import calendar
import datetime
from typing import List, Tuple

from dateutil.parser import parse
from django.db import models

from datetimedim.models.constants import QUARTER_STARTS, QUARTER_NAMES


class DateDimQuerySet(models.QuerySet):
    def weekdays(self):
        return self.filter(day_of_week__in=[1, 2, 3, 4, 5])

    def weekends(self):
        return self.filter(day_of_week__in=[6, 7])

    def year(self, year: int):
        return self.fetch_range(
            start=datetime.date(year, 1, 1),
            end=datetime.date(year, 12, 31),
        )

    def month(self, month, *, year: int = None):
        if year:
            return self.fetch_range(
                start=datetime.date(year, month, 1),
                end=datetime.date(year, month, calendar.monthrange(year, month)[1])
            )
        return self.filter(month=month)

    def day(self, day: int, *, month: int = None, year: int = None):
        if month and year:
            try:
                return self.get(year=year, month=month, day=day)
            except self.model.DoesNotExist:
                self.model.objects.fetch(datetime.date(year, month, day))
        elif month and not year:
            return self.filter(month=month, day=day)
        elif not month and year:
            return self.filter(year=year, day=day)
        elif not month and not year:
            return self.filter(day=day)
        else:
            return False

    def fetch_range(self, *, start: datetime.date, end: datetime.date, inclusive: bool = True,
                    day_of_week_include: List[int] = None, day_of_week_exclude: List[int] = None):
        if inclusive:
            filters = {
                "date_actual__gte": start,
                "date_actual__lte": end
            }
        else:
            filters = {
                "date_actual__gt": start,
                "date_actual__lt": end
            }
        if day_of_week_include:
            filters["day_of_week__in"] = day_of_week_include

        custom_filter = self.filter(**filters)

        if day_of_week_exclude:
            custom_filter = custom_filter.exclude(day_of_week__in=day_of_week_exclude)

        return custom_filter


class DateDimManager(models.Manager):

    def get_queryset(self):
        return DateDimQuerySet(self.model, using=self._db)

    @staticmethod
    def get_day_str(day: int) -> str:
        """
        Converts and pads day number
        :param day: int
        :return: str
        """
        if day < 10:
            return f'0{day}'
        return str(day)

    @staticmethod
    def get_epoch(d: datetime.date) -> int:
        """
        Get days since Jan 01, 0001
        :param d:
        :return: int
        """
        return d.toordinal()

    @staticmethod
    def get_day_name(d: datetime.date) -> str:
        """

        :param d:
        :return:
        """
        return calendar.day_name[calendar.weekday(d.year, d.month, d.day)]

    @staticmethod
    def get_day_abbr(d: datetime.date) -> str:
        """

        :param d:
        :return:
        """
        return calendar.day_abbr[calendar.weekday(d.year, d.month, d.day)]

    @staticmethod
    def get_day_of_week(d: datetime.date) -> int:
        """

        :param d:
        :return:
        """
        return d.isoweekday()

    @staticmethod
    def get_day_of_quarter(d: datetime.date) -> int:
        """

        :param d:
        :return:
        """
        quarter_idx = d.month // 4
        first_month = QUARTER_STARTS[quarter_idx]

        return (d.toordinal() - datetime.date(d.year, first_month, 1).toordinal()) + 1

    @staticmethod
    def get_first_day_of_quarter(d: datetime.date) -> datetime.date:
        """

        :param d:
        :return:
        """
        quarter_idx = d.month // 4
        first_month = QUARTER_STARTS[quarter_idx]
        return datetime.date(
            d.year,
            first_month,
            1
        )

    @staticmethod
    def get_last_day_of_quarter(d: datetime.date) -> datetime.date:
        """

        :param d:
        :return:
        """
        quarter_idx = d.month // 4
        last_month = QUARTER_STARTS[quarter_idx] + 2
        return datetime.date(
            d.year,
            last_month,
            calendar.monthrange(d.year, last_month)[1]
        )

    @staticmethod
    def get_day_of_year(d: datetime.date) -> int:
        """

        :param d:
        :return:
        """
        return int(d.strftime("%j"))

    @staticmethod
    def get_month_str(d: datetime.date) -> str:
        """

        :param d:
        :return:
        """
        if d.month < 10:
            return f'0{d.month}'
        return str(d.month)

    @staticmethod
    def get_week(d: datetime.date, week_starts_on: int = calendar.MONDAY) -> Tuple[List[datetime.date], int]:
        """
        Returns tuple containing a list of dates of that week, and an integer denoting the week in month number
        :param d:
        :param week_starts_on:
        :return:
        """
        weeks = calendar.Calendar(week_starts_on).monthdatescalendar(d.year, d.month)
        i = 1
        for week in weeks:
            if d in week:
                return week, i
            i += 1

    def get_week_of_month(self, d: datetime.date, week_starts_on: int = calendar.MONDAY) -> int:
        return self.get_week(d, week_starts_on=week_starts_on)[1]

    @staticmethod
    def get_quarter_name(quarter: int):
        return QUARTER_NAMES[quarter]

    def get_first_day_of_week(self, d: datetime.date) -> datetime.date:
        """

        :param d:
        :return:
        """
        return self.get_week(d)[0][0]

    def get_last_day_of_week(self, d: datetime.date) -> datetime.date:
        """

        :param d:
        :return:
        """
        return self.get_week(d)[0][-1]

    @staticmethod
    def get_first_day_of_month(d: datetime.date) -> datetime.date:
        """

        :param d:
        :return:
        """
        return datetime.date(d.year, d.month, 1)

    @staticmethod
    def get_last_day_of_month(d: datetime.date) -> datetime.date:
        """

        :param d:
        :return:
        """
        return datetime.date(
            d.year,
            d.month,
            calendar.monthrange(d.year, d.month)[1]
        )

    @staticmethod
    def check_is_weekend(d: datetime.date) -> bool:
        """

        :param d:
        :return:
        """
        return d.isocalendar()[2] == 6 or d.isocalendar()[2] == 7

    def date_exists(self, *, year: int, month: int, day: int):
        """
        Check whether date exists
        :param year: int
        :param month: int
        :param day: int
        :return: bool
        """

        try:
            return self.get(
                year=year,
                month=month,
                day=day
            )
        except self.model.DoesNotExist:
            return False

    def bootstrap(self, years: List[int], week_starts_on: int = calendar.MONDAY) -> None:
        calendar.setfirstweekday(week_starts_on)
        if len(years) > 1:
            for year in range(years[0], years[1] + 1):
                for month in range(1, 13):
                    num_days = calendar.monthrange(year, month)[1]
                    for day in range(1, num_days + 1):
                        d = self.create(
                            year=year,
                            month=month,
                            day=day,
                            week_starts_on=week_starts_on
                        )
                        print(f"Bootstrapping {d}...")
        else:
            year = years[0]
            for month in range(1, 13):
                num_days = calendar.monthrange(year, month)[1]
                for day in range(1, num_days + 1):
                    d = self.create(
                        year=year,
                        month=month,
                        day=day,
                        week_starts_on=week_starts_on
                    )
                    print(f"Bootstrapping {d}...")

    def create(self, *, year: int, month: int, day: int, week_starts_on: int = calendar.MONDAY):
        """

        :param year:
        :param month:
        :param day:
        :param week_starts_on:
        :return:
        """
        date_exists = self.date_exists(year=year, month=month, day=day)
        if date_exists:
            return date_exists
        else:
            date_actual = datetime.date(year=year, month=month, day=day)
            day_str = self.get_day_str(day)
            epoch = self.get_epoch(date_actual)
            day_name = self.get_day_name(date_actual)
            day_abbr = self.get_day_abbr(date_actual)
            day_of_week = self.get_day_of_week(date_actual)
            day_of_month = day
            quarter = (month // 4) + 1
            quarter_name = self.get_quarter_name(quarter)
            day_of_quarter = self.get_day_of_quarter(date_actual)
            day_of_year = self.get_day_of_year(date_actual)
            week_of_month = self.get_week_of_month(date_actual, week_starts_on)
            week_of_year = date_actual.isocalendar()[1]
            month_name = calendar.month_name[month]
            month_abbr = calendar.month_abbr[month]
            month_str = self.get_month_str(date_actual)
            first_day_of_week = self.get_first_day_of_week(date_actual)
            last_day_of_week = self.get_last_day_of_week(date_actual)
            first_day_of_month = self.get_first_day_of_month(date_actual)
            last_day_of_month = self.get_last_day_of_month(date_actual)
            first_day_of_quarter = self.get_first_day_of_quarter(date_actual)
            last_day_of_quarter = self.get_last_day_of_quarter(date_actual)
            first_day_of_year = datetime.date(date_actual.year, 1, 1)
            last_day_of_year = datetime.date(date_actual.year, 12, 31)
            year_actual_iso, week_iso, week_date_iso = date_actual.isocalendar()
            is_weekend = self.check_is_weekend(date_actual)
            nicename_long = f'{day_name}, {month_name} {day}, {year}'
            nicename_short = f'{month_abbr} {day}, {year}'

            d = super(DateDimManager, self).create(
                day=day,
                day_str=day_str,
                date_actual=date_actual,
                epoch=epoch,
                day_name=day_name,
                day_abbr=day_abbr,
                day_of_week=day_of_week,
                day_of_month=day_of_month,
                day_of_quarter=day_of_quarter,
                day_of_year=day_of_year,
                week_of_month=week_of_month,
                week_of_year=week_of_year,
                month=month,
                month_str=month_str,
                month_name=month_name,
                month_abbr=month_abbr,
                quarter=quarter,
                quarter_name=quarter_name,
                year=year,
                first_day_of_week=first_day_of_week,
                last_day_of_week=last_day_of_week,
                first_day_of_month=first_day_of_month,
                last_day_of_month=last_day_of_month,
                first_day_of_quarter=first_day_of_quarter,
                last_day_of_quarter=last_day_of_quarter,
                first_day_of_year=first_day_of_year,
                last_day_of_year=last_day_of_year,
                is_weekend=is_weekend,
                year_actual_iso=year_actual_iso,
                week_iso=week_iso,
                week_date_iso=week_date_iso,
                nicename_long=nicename_long,
                nicename_short=nicename_short
            )

            return d

    def fetch(self, d):
        """
        Fetch DateDim object based on d, which can be:
        - str: parsable by dateutil.parser
        - datetime.date object
        - datetime.datetime object
        - DateDim object
        - int: number of days since Jan 1, 0001
        :param d:
        :return: DateDim
        """
        if isinstance(d, str):
            try:
                d = parse(d).date()
            except ValueError as e:
                return e
        elif isinstance(d, datetime.date):
            pass
        elif isinstance(d, datetime.datetime):
            d = d.date()
        elif isinstance(d, self.model):
            return d
        elif isinstance(d, int):
            d = datetime.date.fromordinal(d)
        else:
            raise ValueError(f"Invalid format: {d}")

        try:
            __date = self.get(date_actual=d)
        except self.model.DoesNotExist:
            __date = self.create(
                year=d.year,
                month=d.month,
                day=d.day
            )

        return __date

    def fetch_range(self, *, start: datetime.date, end: datetime.date, inclusive: bool = True,
                    day_of_week_include: List[int] = None, day_of_week_exclude: List[int] = None, safe=False):
        """
        Fetch a range of DateDims from start to end
        :param start:
        :param end:
        :param inclusive:
        :param day_of_week_include:
        :param day_of_week_exclude:
        :param safe:
        :return:
        """
        if start >= end:
            raise ValueError(f"Start date {start} can't be greater than or equal to end date {end}!")

        if safe:
            try:
                __start = self.get(date_actual=start)
            except self.model.DoesNotExist:
                __start = self.create(year=start.year, month=start.month, day=start.day)

            try:
                __end = self.get(date_actual=end)
            except self.model.DoesNotExist:
                __end = self.create(year=end.year, month=end.month, day=end.day)

            current_datedim = __start
            while current_datedim.epoch < __end.epoch:
                current_datedim = current_datedim.tomorrow()

        return self.get_queryset().fetch_range(
            start=start,
            end=end,
            inclusive=inclusive,
            day_of_week_exclude=day_of_week_exclude,
            day_of_week_include=day_of_week_include
        )

    def year(self, year: int):
        """

        :param year:
        :return:
        """
        return self.get_queryset().year(year)

    def month(self, month, *, year: int = None):
        """

        :param month:
        :param year:
        :param safe:
        :return:
        """

        return self.get_queryset().month(month, year=year)

    def day(self, day: int, *, month: int = None, year: int = None):
        """

        :param day:
        :param year:
        :param month:
        :param safe:
        :return:
        """
        return self.get_queryset().day(day, month=month, year=year)

    def weekdays(self):
        return self.get_queryset().weekdays()

    def weekends(self):
        return self.get_queryset().weekends()
