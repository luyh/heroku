from pytz import timezone
from datetime import datetime

cst_tz = timezone('Asia/Shanghai')
utc_tz = timezone('UTC')
utcnow = datetime.utcnow().replace(tzinfo=utc_tz)
china = utcnow.astimezone(cst_tz).strftime('%Y-%m-%d %H:%M:%S')
print(china,'python demo.py')