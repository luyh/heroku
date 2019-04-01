from pytz import timezone
from datetime import datetime

def getChinaTime():
    cst_tz = timezone('Asia/Shanghai')
    utc_tz = timezone('UTC')
    utcnow = datetime.utcnow().replace(tzinfo=utc_tz)
    china = utcnow.astimezone(cst_tz).strftime('%Y-%m-%d %H:%M:%S')
    return china

if __name__ == '__main__':
    print(getChinaTime())