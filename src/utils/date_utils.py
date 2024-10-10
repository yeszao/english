from datetime import datetime, timedelta


def get_now_filename():
    return datetime.now().strftime("%Y%m%d%H%M%S")


def get_today():
    return datetime.now().strftime("%Y-%m-%d")


def get_yesterday():
    return (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")


def str_to_datetime(date_str):
    return datetime.strptime(date_str, "%m/%d/%Y, %I:%M %p, %z UTC")
