import math
import queue
import Adafruit_ADS1x15

# GPIO 3, 5 used  (I2C)
adc    = Adafruit_ADS1x15.ADS1015()  # ADS converter type no.
pt100A = 3.9083e-3                   # Pt100 redister to temprature convert const.
cTerm  = -2.0                        # Correction term
pt100Tmp = 0.0                       # Temprature global val.

GAIN = 1                             # ADS gain (Needing more info, see Adafruit site)

tmpQ = queue.Queue()                 # Temp. history queue

def tempCalc(val):                   # Convert resister val. to temp.
    global pt100Tmp, tmpQ
    prevt = 0.0

    tp = (val-100.0) / (100*pt100A) + cTerm
    tmpQ.put(tp)
    n = tmpQ.qsize()
    if n>10:
        prevt = tmpQ.get()
        pt100Tmp = (pt100Tmp*(n-1) - prevt + tp) / (n-1)
    else:
        pt100Tmp = (pt100Tmp*(n-1) + tp) / n
    return round(pt100Tmp, 1)

def pt100GetTmp(): # get Temp. data from Pt100
    pt100E = adc.read_adc(0, gain=GAIN)
    pt100EBase = adc.read_adc(1, gain=GAIN)

    if pt100E == 0:
        r = 10e9+7
    else:
        r = pt100EBase*100.0 / pt100E - 100.0

    return tempCalc(r)
