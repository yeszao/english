from datetime import datetime, timedelta


def get_today():
    return datetime.now().strftime("%Y-%m-%d")


def get_yesterday():
    return (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")

