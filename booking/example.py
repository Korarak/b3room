from datetime import time
from datetime import datetime
from thai_strftime import *
datetime_obj = datetime(year=1976, month=10, day=6)
xx = thai_strftime(datetime_obj, "%a %-d %b %y")
print(xx)