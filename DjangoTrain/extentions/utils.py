from . import jalali
from django.utils import timezone

def number_conventor(mystr):
    numbers = {
        "1" : "۱" ,
        "2" : "۲" ,
        "3" : "۳" ,
        "4" : "۴" ,
        "5" : "۵" ,
        "6" : "۶" ,
        "7" : "۷" ,
        "8" : "۸" ,
        "9" : "۹" ,
        "0" : "۰" ,
    }

    for enum , pnum in numbers.items():
        mystr = mystr.replace(enum , pnum)
    return mystr

def jalali_conventor(time):
    jmonths = ["فروردین" , "اردیبهشت" , "خرداد" , "تیر" , "مرداد" , "شهریور" , "مهر" , "آبان" , "آذر" , "دی" , "بهمن" , "اسفند"]

    time = timezone.localtime(time)

    time_to_str = "{},{},{}".format(time.year , time.month , time.day)
    time_to_tuple = jalali.Gregorian(time_to_str).persian_tuple()

    time_to_list = list(time_to_tuple)

    for index , month in enumerate(jmonths):
        if time_to_list[1] == index + 1 :
            time_to_list[1] = month
            break

    output = "{}/{}/{}  , ساعت {}:{} ".format(
        time_to_list[2],
        time_to_list[1],
        time_to_list[0],
        time.hour,
        time.minute,
    )

    return number_conventor(output)