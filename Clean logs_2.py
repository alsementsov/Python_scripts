import pylab
import numpy as np
import matplotlib.pyplot as plt

pdata = np.genfromtxt('log_3.txt') 
size_data=np.shape(pdata)
N=size_data[0]

fdata=[]

prev=pdata[0,0]

# Убрать провалы
for sample in pdata:
    if (sample[0]>90000):
        fdata.append(sample[0])
        prev=sample[0]
    else:
        fdata.append(prev)
  
plt.plot(pdata[:,0],color='red',linewidth=1.5)
plt.grid(True)
plt.xticks(np.arange(0, N, step=25))
## Нужно корректировать вручную границы графика
plt.ylim(90000,92500)
plt.xlim(125,550)

plt.plot(fdata,color='blue',linewidth=2.5)

figManager = plt.get_current_fig_manager()
figManager.window.showMaximized()
plt.tight_layout()
plt.show()
