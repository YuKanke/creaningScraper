from time import sleep
import datetime
import csv
import getHakuyosha

functions = {getHakuyosha.main}

with open('./cleaningShops_' + datetime.datetime.now().strftime('%Y%m%d%H%M%S') + '.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    for func in functions:
        sleep(5)
        output = func()
        writer.writerow(output)
