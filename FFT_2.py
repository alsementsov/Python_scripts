import pylab
import numpy as np
import matplotlib.pyplot as plt
import scipy.fftpack
from scipy.fftpack import rfft, irfft, fftfreq
from scipy.signal import find_peaks


pdata = np.genfromtxt('log_2.log') 
pdata = pdata[6:]
mean_removed = np.ones_like(pdata)*np.mean(pdata)
pdata_norm = pdata - mean_removed
#yf = rfft(a=pdata_norm)
yf = np.fft.rfft(a=pdata_norm)
yf = np.abs(yf)
peaks, properties = find_peaks(pdata_norm, prominence=1, width=4)


plt.subplot(121)
plt.grid(axis='both')
plt.plot(pdata)
plt.plot(peaks, pdata_norm[peaks], "x")
plt.subplot(122)
plt.xlim((0, 100)) 
plt.ylim((0, 100000)) 
plt.plot(yf)
xaxisticker = np.linspace(0, 100,endpoint=False, num=20)
pylab.xticks(xaxisticker)
plt.grid(axis='both')
plt.plot()



