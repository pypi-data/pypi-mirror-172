import time 

def Size(ByteNumber, suffix='B'):
    for unit in ['','K','M','G','T','P','E','Z']:
        if abs(ByteNumber) < 1024.0:
            return "%3.1f%s%s" % (ByteNumber, unit, suffix)
        ByteNumber /= 1024.0
    return "%.1f%s%s" % (ByteNumber, 'Y', suffix)

def TimeDuration(seconds:int) -> str:
    return time.strftime("%H:%M:%S", time.gmtime(seconds))