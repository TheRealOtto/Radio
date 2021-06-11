from time import strftime, sleep
clr_fctr = 9 

for hor in range (0, 2400, 100):
    for mnt in range (60):
        tme = round(hor+mnt*1.666666, 0)

        print("Time: ", hor+mnt, tme)

        if tme < 1200:
            color = int((tme/100)**2*clr_fctr)
        elif tme >= 1200:
            color = int((24 - (tme/100))**2*clr_fctr)

        if color > 1279:
            color = 1279
        if color < 1:
            color = 1
        print("Color: ", color)

        sleep(0.1)
