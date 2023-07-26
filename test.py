series = [1, 5, 4, 2, 3, 5, 4, 3, 2, 1]

ave = None
for i, x in enumerate(series):
    if ave is None:
        ave = x
    else:
        multiplier = 1 / (i + 1)
        ave = ave + (multiplier * (x - ave))

    print('Average is now ' + str(ave))

print(ave)
