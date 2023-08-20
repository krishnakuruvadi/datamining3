import datetime
from dateutil.relativedelta import relativedelta
from dateutil import tz
from pytz import timezone

def get_float_or_zero_from_string(input):
    if input != None and input != '':
        try:
            res = float(input)
            return res
        except Exception as e:
            print('error converting ', input, ' to float. returning 0')
    return 0

def get_float_or_none_from_string(input, printout=True):
    if input != None and input != '':
        try:
            res = float(input)
            return res
        except Exception as e:
            if printout:
                print('error converting ', input, ' to float. returning none')
    return None

def get_int_or_none_from_string(input):
    if input != None and input != '':
        try:
            res = int(input)
            return res
        except Exception as e:
            print('error converting ', input, ' to int. returning none')
    return None

# default format expected of kind 2020-06-01
def get_datetime_or_none_from_string(input, format='%Y-%m-%d'):
    if input != None and input != '':
        try:
            res = datetime.datetime.strptime(input, format)
            return res
        except Exception as e:
            print(f'error converting {input} to date using format {format}. returning none')
    return None

# default format expected of kind 2020-06-01
def get_date_or_none_from_string(input, format='%Y-%m-%d', printout=True):
    if input != None and input != '':
        try:
            res = datetime.datetime.strptime(input, format).date()
            return res
        except Exception as e:
            if printout:
                print('error converting ', input, ' to date. returning none' + str(e))
    return None

def convert_date_to_string(input, format='%Y-%m-%d'):
    return input.strftime(format)

def get_diff(x,y):
    if x>y:
        return x-y
    return y-x

def get_in_preferred_tz(utc_date_time):
    #from common.helper import get_preferences

    from_zone = tz.tzutc()
    utc_date_time = utc_date_time.replace(tzinfo=from_zone)
    #preferred_tz = get_preferences('timezone')
    #if not preferred_tz:
    #    preferred_tz = 'Asia/Kolkata'
    preferred_tz = 'Asia/Kolkata'
    return utc_date_time.astimezone(timezone(preferred_tz)).strftime("%Y-%m-%d %H:%M:%S")
    
def k_obfuscate(byt):
    # Use same function in both directions.  Input and output are bytes
    # objects.
    mask = b'keyword'
    lmask = len(mask)
    return bytes(c ^ mask[i % lmask] for i, c in enumerate(byt))

def k_decode(data):
    return k_obfuscate(data).decode()

def get_min(a, b):
    if not a:
        return b
    if not b:
        return a
    return a if a<b else b

def get_max(a, b):
    if not a:
        return b
    if not b:
        return a
    return a if a>b else b