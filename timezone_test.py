import datetime
import pytz

def check_timezone():
    # Noncompliant: Using pytz.timezone directly in the constructor can lead to incorrect results
    dt = datetime.datetime(2022, 1, 1, tzinfo=pytz.timezone('US/Eastern'))
    print(dt)
