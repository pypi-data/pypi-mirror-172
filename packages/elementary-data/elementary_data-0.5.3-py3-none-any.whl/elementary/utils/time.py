from datetime import datetime, timezone
from typing import Optional

from dateutil import tz

MILLISECONDS_IN_SEC = 1000
MILLISECONDS_IN_MIN = 1000 * 60
MILLISECONDS_IN_HOUR = 1000 * 60 * 60

DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S"


def convert_utc_time_to_timezone(
    utc_time: datetime, timezone: Optional[str] = None
) -> datetime:
    from_zone = tz.tzutc()
    to_zone = tz.gettz(timezone) if timezone else tz.tzlocal()
    utc_time = utc_time.replace(tzinfo=from_zone)
    return utc_time.astimezone(to_zone)


def get_now_utc_str(format: str = DATETIME_FORMAT) -> str:
    return datetime.utcnow().strftime(format)


def get_now_utc_iso_format() -> str:
    return datetime.now(timezone.utc).isoformat()


def format_milliseconds(duration: int) -> str:
    seconds = int((duration / MILLISECONDS_IN_SEC) % 60)
    minutes = int((duration / MILLISECONDS_IN_MIN) % 60)
    hours = int(duration / MILLISECONDS_IN_HOUR)

    remaining_milliseconds = duration - (
        hours * MILLISECONDS_IN_HOUR
        + minutes * MILLISECONDS_IN_MIN
        + seconds * MILLISECONDS_IN_SEC
    )

    return f"{hours}h:{minutes}m:{seconds}s:{remaining_milliseconds}ms"


def convert_datetime_utc_str_to_timezone_str(
    isoformat_datetime: str, timezone: Optional[str]
) -> str:
    try:
        parsed_time = datetime.fromisoformat(isoformat_datetime)
        return convert_utc_time_to_timezone(parsed_time, timezone).strftime(
            DATETIME_FORMAT
        )
    except Exception:
        return isoformat_datetime
