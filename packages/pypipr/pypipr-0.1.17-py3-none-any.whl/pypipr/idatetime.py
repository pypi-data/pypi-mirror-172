IDATETIME = True

"""PYPIPR Module"""


"""PYTHON Standard Module"""
import datetime
import zoneinfo


"""PYPI Module"""
import pytz


def datetime_now(timezone=None):
    """
    Datetime pada timezone tertentu
    """
    tz = pytz.timezone(timezone) if timezone else None
    return datetime.datetime.now(tz)
    # return datetime.datetime.now(zoneinfo.ZoneInfo(timezone))


def datetime_from_string(str):
    """
    Fungsi ini dapat memparse segala jenis string kemudian akan
    mengembalikan python datetime class
    """
    pass
