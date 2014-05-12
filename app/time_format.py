import math

place_vals = [1000, 60000, 3600000]


def num_to_string(num):
    ms = num % 1000
    num = math.floor(num/1000)
    s = num % 60
    num = math.floor(num/60)
    m = num % 60
    h = math.floor(num/60)
    return "%02d:%02d:%02d.%03d" % (h, m, s, ms)


def string_to_num(str):
    restimes = 0
    mainsects = str.split(".")
    if len(mainsects) > 1:
        restimes += int(mainsects[1])
    othsec = mainsects[0].split(":")
    othsec = othsec[::-1]
    for i in range(len(othsec)):
        restimes += (int(othsec[i])*place_vals[i])
    return restimes
