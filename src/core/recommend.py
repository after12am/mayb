import os, sys
from math import sqrt
from db import SQLite3
from db.mapper import Pins, Words, Clusters
from datetime import datetime

def pearson(x, y):
    n = len(x)
    sumx = sum(x)
    sumy = sum(y)
    # sum of the squares
    sumxSq = sum([pow(v, 2) for v in x])
    sumySq = sum([pow(v, 2) for v in y])
    # sum of the products
    pSum = sum([x[i] * y[i] for i in range(n)])
    # calculate pearson score
    num = pSum - (sumx * sumy / n)
    den = sqrt((sumxSq - pow(sumx, 2) / n) * (sumySq - pow(sumy, 2) / n))
    if den == 0: return 0
    return 1.0 - num / den

def cluster(similarity=pearson):
    db = SQLite3().cursor()
    pins = Pins()
    words = Words()
    maxcount = pins.size()
    labels = [r[0] for r in words.set()]
    offset = 0
    n = 1
    sum_num = sum([i for i in range(1, maxcount)])
    while True:
        pin_a = pins.find_by_offset(offset)
        pin_a_words = [w[0] for w in words.find_by_pinid(pin_a[0])]
        pin_a_wordcount = [pin_a_words.count(w) for w in list(set(labels))]
        # calculate distance of two pins.
        for i in range(offset + 1, maxcount):
            pin_b = pins.find_by_offset(i)
            pin_b_words = [w[0] for w in words.find_by_pinid(pin_b[0])]
            pin_b_wordcount = [pin_b_words.count(w) for w in list(set(labels))]
            # calculate distance of two pins
            print '[%s] %s / %s calculate score of %s and %s' % (datetime.today().strftime('%Y-%m-%d %H:%M:%S'), n, sum_num, pin_a[0], pin_b[0])
            sim = 1.0 - similarity(pin_a_wordcount, pin_b_wordcount)
            # save distance to database for cache
            clusters = Clusters()
            clusters.data['pin_id_a'] = pin_a[0]
            clusters.data['pin_id_b'] = pin_b[0]
            clusters.data['score'] = sim
            clusters.save()
            n += 1
        if offset >= maxcount - 1:
            break
        offset += 1

# def get_top_matches(data, pin_id, m=5, similarity=pearson):
#     target = []
#     for pin in data:
#         if pin[0] == pin_id:
#             target = pin[1:]
#             break
#     scores = []
#     for pin in data[1:]:
#         if pin[0] != pin_id:
#             scores.append((1.0 - similarity(pin[1:], target), pin[0]))
#     scores.sort()
#     scores.reverse()
#     return scores[:m]

def main():
    pass

if __name__ == '__main__': main()