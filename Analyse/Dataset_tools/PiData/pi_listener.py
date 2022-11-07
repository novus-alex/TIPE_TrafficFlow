from datetime import datetime, date
import time, os
from xml_to_csv import *

while True:
    now = datetime.now()
    if not os.path.exists(date.today().strftime("%m/%d/%y")):
        os.mkdir(date.today().strftime("%m/%d/%y"))

    if int(now.strftime("%M")) % 30 != 0:
        data = XML(BF.xml_url)
        data.parse_xml()
        data.to_csv(f'bf_dataset/{date.today().strftime("%m/%d/%y")}/{now.strftime("%H_%M_%S")}.csv')
        print(f'{date.today().strftime("%m/%d/%y")} - {now.strftime("%H:%M:%S")}]: Saving data.')
        time.sleep(60)