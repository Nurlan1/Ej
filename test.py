import datetime
import time
def calculate():
#     d = datetime.date(2018, 4, 16)
#     print(d)
#     next_monday = next_weekday(d, 0)  # 0 = Monday, 1=Tuesday, 2=Wednesday...
#     print(next_monday)
#
#
# def next_weekday(d, weekday):
#     days_ahead = weekday - d.weekday()
#     if days_ahead <= 0:  # Target day already happened this week
#         days_ahead += 7
#     return d + datetime.timedelta(days_ahead)
    orig = datetime.datetime.fromtimestamp(1523852949)
    new = orig + datetime.timedelta(days=0)
    print(new.timestamp())

if __name__ == '__main__':

    calculate()