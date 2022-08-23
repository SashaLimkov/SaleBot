from datetime import datetime, timedelta


async def get_datetime(key):
    day = datetime.today()
    today = datetime(day.year, day.month, day.day)
    if key == "today":
        return datetime(today.year, today.month, today.day)
    elif key == "yesterday":
        yesterday = today - timedelta(days=1)
        return datetime(yesterday.year, yesterday.month, yesterday.day)
    else:
        tomorrow = today + timedelta(days=1)
        return datetime(tomorrow.year, tomorrow.month, tomorrow.day)

