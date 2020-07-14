from time import sleep
import datetime
import csv
import getHakuyosha
import getCleaningSenka
import getPonyCleaning
import getKikuya

# functions = {'白洋舎' : getHakuyosha.main, 'クリーニング専科' : getCleaningSenka.main, 'ポニークリーニング' : getPonyCleaning.main, '喜久屋' : getKikuya.main, 'ノムラクリーニング' : getNomuraCleaning.main}

functions = {'ノムラクリーニング' : getNomuraCleaning.main}
for key, value in functions.items():
    with open('./cleaningShops_' + key + '_' + datetime.datetime.now().strftime('%Y%m%d%H%M%S') + '.csv', 'w', newline='') as f:
        sleep(5)
        output = value()
        writer = csv.writer(f)
        writer.writerows(output)
