from time import sleep
import datetime
import csv
import getHakuyosha
import getCleaningSenka

functions = {'白洋舎' : getHakuyosha.main, 'クリーニング専科' : getCleaningSenka.main}

for key, value in functions.items():
    with open('./cleaningShops_' + key + '_' + datetime.datetime.now().strftime('%Y%m%d%H%M%S') + '.csv', 'w', newline='') as f:
        sleep(5)
        output = value()
        writer = csv.writer(f)
        writer.writerows(output)
