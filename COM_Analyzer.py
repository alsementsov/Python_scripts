import serial
import numpy as np
import matplotlib.ticker
import matplotlib.pyplot as plt
import scipy.fftpack
from scipy.fftpack import rfft, irfft, fftfreq
from scipy.signal import find_peaks
import pylab

Filename = "log_5"

ard=serial.Serial('COM3',115200)
ard.timeout = 1 # in seconds
logfile=open(Filename+'.log',"w")
cnt = 0
while (cnt<261):
    x = ard.readline()
    if len(x) == 0:
        break
    s = str(x)
    s=s[2:]
    i=1
    stemp=s[:i]
    while stemp.isdigit():
        i=i+1
        stemp=s[:i]
    if (i>1):
        s=stemp[:i-1]
        logfile.write(s+'\n')
    cnt=cnt+1
    print(cnt)
logfile.close()
ard.close()
print("stop")
##########################################################################################
# Analyze
##########################################################################################
pdata = np.genfromtxt(Filename+'.log') 
pdata = pdata[6:]
mean_removed = np.ones_like(pdata)*np.mean(pdata)
pdata_norm = pdata - mean_removed
yf = np.fft.rfft(a=pdata_norm)
yf = np.abs(yf)
peaks, properties = find_peaks(pdata_norm, prominence=1, width=4)

plt.subplot(121)
plt.grid(axis='both')
plt.plot(pdata_norm)
plt.plot(peaks, pdata_norm[peaks], "x")
plt.subplot(122)
plt.xlim((0, 150)) 
plt.ylim((1, 200000)) 
plt.plot(yf)
xaxisticker = np.linspace(0, 150,endpoint=False, num=15)
pylab.xticks(xaxisticker)
plt.grid(axis='both',linestyle = '--')
plt.plot()
plt.savefig(Filename+'.png',quality =95,dpi=300)
