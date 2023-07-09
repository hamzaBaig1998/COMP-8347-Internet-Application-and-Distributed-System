import datetime

print("1 a")
#Take input from user
date_in=input("Enter date in MM/DD/YYYY format: ")

#1 a
#convert to datetime object
date_obj=datetime.datetime.strptime(date_in, "%m/%d/%Y")

print("date_object: ",date_obj)


print("1 b")
#1 b
#convert format of datetime_obj
date_obj = datetime.datetime.now() # current date and time
date_obj_update=date_obj.strftime("%Y-%m-%d %H:%M:%S")

print("datetime object: ",date_obj)
print("updated datetime object: ",date_obj_update)

print("1 c")
#1 c
# return date and time as separate strings
date_obj = datetime.datetime.now() # current date and time
date_obj_date=date_obj.strftime("%Y-%m-%d")
print("datetime object: ",date_obj)
print("date: ",date_obj_date)

date_obj_time=date_obj.strftime("%H:%M:%S")
print("time: ",date_obj_time)

print("1 d")
print("Please make sure second date is bigger than the first")
date_one=input("Enter date One in MM/DD/YYYY format: ")
date_two=input("Enter date Two in MM/DD/YYYY format: ")

#converting dates
date_one= datetime.datetime.strptime(date_one, "%m/%d/%Y")
date_two=datetime.datetime.strptime(date_two, "%m/%d/%Y")

#calculating difference
days_difference=day = date_two - date_one

print("The number days difference between the given dates is: ",days_difference.days)


print("1 e")
date_obj = datetime.datetime.now() # current date and time

days_to_add=int(input("Enter the number of days you want to add to today's date: "))

print("Date before update: ",date_obj)

date_obj=date_obj + datetime.timedelta(days=days_to_add)

print("Date after update: ",date_obj)

