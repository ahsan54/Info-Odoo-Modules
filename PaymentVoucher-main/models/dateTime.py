from datetime import datetime,date,timedelta
from time import strftime
from dateutil.relativedelta import relativedelta

#-> System Default Print:- 2024-10-28


# print(date.today())
# print('Today: ',datetime.today())
# print('Now: ',datetime.now())
#
# Chk krne ke liye 1st format ma KrLo 1st date ko
# if date.today().strftime('%Y-%m-%d') == '2024-10-28':
#     print('Today: True')
#
# Any:
# if date.today().strftime('%d-%m-%Y') == '28-10-2024':
#     print('Today: True')
#
#
# ##########################----- Convert DateTime TO Date: --------->
#
# dt = datetime.now()
# dt_to_date = dt.date()
# print('DT To Date:- ',dt_to_date) # 2024-10-28
#
#
#
# ##########################----- Convert Date To DateTime: --------->
#
# d = date.today()
# d_to_midNightTime = datetime.combine(d,datetime.min.time())
# print('Mid Night: ',d_to_midNightTime) # 2024-10-28 00:00:00
# # OR
# d_to_dateTime = datetime.combine(d,datetime.max.time())
# print('Max Time: ',d_to_dateTime) # 2024-10-28 23:59:59.999999
# # OR
# d_to_Time_Now = datetime.combine(d,datetime.now().time())
# print('Current Time: ',d_to_Time_Now) # 2024-10-28 16:44:28.807604
#
#
# ##########################--------------- # ---> Str_P_Time
# string parse time
# Uses: when you have a date or time in string format and want to convert it to a datetime object
#
#
# String_Time = "2024-10-28"
# print(type(String_Time)) # <class 'str'>
# date_obj = datetime.strptime(String_Time, "%Y-%m-%d")
# print(type(date_obj)) # <class 'datetime.datetime'>
#
#
#
#
# # Add Days : -
#
# add_days = date.today() + timedelta(days=5)
# print(add_days)
#
# add_custom_days = datetime.strptime('2024-10-28','%Y-%m-%d') + timedelta(days=5)
# print(add_custom_days)
#
#
# # Add months years : Using RelativeDelta function
#
# add_custom_months = datetime.strptime('12-12-2024','%d-%m-%Y') + relativedelta(months=1)
# print(add_custom_months)
#
# add_custom_years = datetime.strptime('12-12-2012','%d-%m-%Y') + relativedelta(years=12)
# print(add_custom_years)
#
#
# # Adding In Time : By TimeDelta , 2 uses of timeDelta
#
# add_time = datetime.now() + timedelta(hours=8 , minutes=30 , seconds=0)
# print('Time: ',add_time)
#
# add_custom_time =  datetime.strptime('2024-10-28 17:51:00', '%Y-%m-%d %H:%M:%S') + timedelta(hours=8 , minutes=30 , seconds=0)
# print('Custom Time: ',add_custom_time)
# #
#


add_today = datetime.strptime('29-10-2020','%d-%m-%Y') + timedelta(days=date.today().weekday())
print(add_today)













