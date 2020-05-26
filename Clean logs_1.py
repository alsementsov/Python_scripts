import pylab
import numpy as np
import matplotlib.pyplot as plt

text_file = open("putty3.log", "r")
lines = text_file.readlines()

# Убрать провалы
for tline in lines:
    if (tline[:5]=='spo2:'):
          a=tline.replace('spo2: ','')
          a=a.replace('hr: ','')
          spo2_hr=a.split(',')
          SPO2.append(int(spo2_hr[0])/100)
          HR.append(int(spo2_hr[1]))
          print(spo2_hr)
    elif (tline[:5]=='red: '):
        a=tline.replace('red: ','')
        red_ir = a.split('ir: ')
        RED.append(int(red_ir[0]))
        IR.append(int(red_ir[1]))
        
plt.plot(RED)  


figManager = plt.get_current_fig_manager()
figManager.window.showMaximized()
plt.tight_layout()
plt.show()
