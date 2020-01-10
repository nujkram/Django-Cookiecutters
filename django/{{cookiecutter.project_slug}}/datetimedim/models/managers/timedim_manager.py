import datetime

import pytz
from dateutil.parser import parse
from django.db import models


class TimeDimQuerySet(models.QuerySet):
    def morning(self, tz='utc'):
        if tz:
            noon = datetime.time(12, 0).replace(tzinfo=pytz.timezone(tz))
        else:
            noon = datetime.time(12, 9)
        return self.filter(
            time_actual__lt=noon,
        )

    def afternoon(self, tz='utc'):
        if tz:
            noon = datetime.time(12, 0).replace(tzinfo=pytz.timezone(tz))
            evening = datetime.time(18, 0).replace(tzinfo=pytz.timezone(tz))
        else:
            noon = datetime.time(12, 0)
            evening = datetime.time(18, 0)
        return self.filter(
            time_actual__gt=noon,
            time_actual__lt=evening
        )

    def evening(self, tz='utc'):
        if tz:
            evening = datetime.time(18, 0).replace(tzinfo=pytz.timezone(tz))
        else:
            evening = datetime.time(18, 0)
        return self.filter(
            time_actual__gte=evening
        )

    def fetch_range(self, *,
                    start: datetime.time,
                    end: datetime.time,
                    inclusive: bool = True,
                    tz: str = None):
        if tz:
            start = start.replace(tzinfo=pytz.timezone(tz))
            end = end.replace(tzinfo=pytz.timezone(tz))

        if inclusive:
            filters = {
                "time_actual__gte": start,
                "time__actual__lte": end
            }
        else:
            filters = {
                "time_actual__gt": start,
                "time__actual__lt": end
            }

        return self.filter(**filters)


class TimeDimManager(models.Manager):
    def get_queryset(self):
        return TimeDimQuerySet(self.model, using=self._db)

    def morning(self, tz='utc'):
        return self.get_queryset().morning(tz)

    def afternoon(self, tz='utc'):
        return self.get_queryset().afternoon(tz)

    def evening(self, tz='utc'):
        return self.get_queryset().evening(tz)

    def get_hour_str(self, h: int) -> str:
        """

        :param h:
        :return:
        """
        if h < 10:
            return f'0{h}'
        return f'{h}'

    def get_minute_str(self, m: int) -> str:
        """

        :param m:
        :return:
        """
        if m < 10:
            return f'0{m}'
        return f'{m}'

    def time_exists(self, *, h: int, m: int) -> bool:
        """

        :param h:
        :param m:
        :return:
        """
        try:
            return self.get(
                hour=h,
                minute=m
            )
        except self.model.DoesNotExist:
            return False

    def create(self, *, h: int, m: int):
        """

        :param h:
        :param m:
        :return:
        """
        time_exists = self.time_exists(h=h, m=m)
        if time_exists:
            return time_exists

        time_actual = datetime.time(h, m)
        hour = h
        minute = m
        hour_str = time_actual.strftime("%H")
        hour_12 = int(time_actual.strftime("%I"))
        hour_12_str = int(time_actual.strftime("%I"))
        minute_str = time_actual.strftime("%M")
        minute_of_day = (datetime.timedelta(hours=time_actual.hour, minutes=time_actual.minute) - datetime.timedelta(
            hours=0, minutes=0)).seconds // 60
        am_pm = time_actual.strftime("%p")

        t = super(TimeDimManager, self).create(
            time_actual=time_actual,
            hour=hour,
            minute=minute,
            hour_str=hour_str,
            hour_12=hour_12,
            hour_12_str=hour_12_str,
            minute_str=minute_str,
            minute_of_day=minute_of_day,
            am_pm=am_pm,
        )

        return t

    def bootstrap(self):
        for h in range(0, 24):
            for m in range(0, 60):
                t = self.create(h=h, m=m)
                print(f"Bootstrapping {t}")

    def fetch(self, t, *, tz=None):
        """
        Fetch TimeDim object based on t, which can be:
        - str: parsable by dateutil.parser
        - datetime.datetime object
        - TimeDim object
        - int: number of minutes since midnight
        :param tz:
        :param t:
        :return: TimeDim
        """

        if isinstance(t, str):
            t = parse(t).time()
        elif isinstance(t, datetime.time):
            pass
        elif isinstance(t, datetime.datetime):
            t = t.time()
        elif isinstance(t, self.model):
            return t
        elif isinstance(t, int):
            if t > 1440 or t < 0:
                t = t % 1440

            h = t // 60
            m = t % 60
            t = datetime.time(h, m)
        else:
            raise ValueError(f"Unknown input: {t}")

        if tz:
            t = t.replace(tzinfo=pytz.timezone(tz))

        try:
            __time = self.get(hour=t.hour, minute=t.minute)
        except self.model.DoesNotExist:
            raise ValueError(f"Invalid time: {t}, {type({t})}")

        return __time

    def fetch_range(self, *,
                    start: datetime.time,
                    end: datetime.time,
                    inclusive: bool = True,
                    tz: str = None):
        """
        Fetch a range of times between start and end
        :param tz:
        :param start:
        :param end:
        :param inclusive:
        :return:
        """

        return self.get_queryset().fetch_range(
            start=start,
            end=end,
            inclusive=inclusive,
            tz=tz
        )
