from datetime import datetime
import time
from xml_to_csv import *

count = 0
while count < 20:
    now = datetime.now()
    if int(now.strftime("%M")) % 10 == 0:
        data = XML(BF.xml_url)
        data.parse_xml()
        data.to_csv(f'bf_dataset/{now.strftime("%H_%M_%S")}.csv')
        print(f"Saving data from {now.strftime('%H_%M_%S')}")
        count += 1
        time.sleep(60)
        
print("ok !")