import numpy as np
import cv2
Xstart = 200
Xend = 300
Ystart = 400
Yend = 500
Xj_start = 353
Xj_end = 823 # Ширина = 470
Yj_start = 140
Yj_end = 400 # Высота = 270
# Correlation function------------------
vid = cv2.VideoCapture('D:\JETS\jet2.mp4') 
#fourcc = cv2.VideoWriter_fourcc(*'MJPG')
#outvid = cv2.VideoWriter('D:\JETS\jet4_plus.avi', fourcc, 20.0, (960,540))  
Step = True
start = True
ByStep_mode = True
Nframe = 0
Sumt = 0
Summa_dx = 0
Summa_dy = 0
ROI_prev = np.zeros((470,250),dtype=np.int16)
#cv2.useOptimized
while(vid.isOpened()):
    key = cv2.waitKey(1) & 0xFF 
    if key == ord('q'):
        break
    elif key == ord('w'):
        Step=True
    elif key == ord('e'):
        ByStep_mode= not ByStep_mode
        if not ByStep_mode:
            Step=True
    if Step:
        Nframe +=1
        if ByStep_mode:
            Step = False
        try:
            ret,frame = vid.read() #Чтение кадра
            if not ret:
                break
        except: 
            break
        # HSV ---------------------------------------
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        Hue,Saturation,img = cv2.split(hsv)
        if start:
            H = np.size(frame, 0)
            W = np.size(frame, 1)
            S = H*W
            start  = False
            etalon = np.asarray(img[Ystart:Yend,Xstart:Xend])
            ROI_prev = np.asarray(img[Yj_start: Yj_end, Xj_start: Xj_end ])
        # Вырезаем кусок для стабилизации
        dy_shift = 0
        dx_shift = 0
        first = True
        for dy in range(-10,10):
            for dx in range(-10,10):
                current = np.asarray(img[Ystart+dy:Yend+dy,Xstart+dx:Xend+dx])
                Summa=0;
                delta = (np.subtract(etalon,current,dtype = 'int16'))**2
                #print("etalon=",etalon)
                #print("current=",current)
                #print("delta=",delta)
                Summa = np.sum(delta,dtype = 'uint32')
                if first:
                    Summa_min = Summa
                    first = False
                    dx_shift = dx
                    dy_shift = dy
                elif (Summa < Summa_min):
                    Summa_min = Summa
                    dx_shift = dx  
                    dy_shift = dy
        etalon = np.asarray(img[Ystart:Yend,Xstart:Xend])
        #print("dx = ",dx_shift)
        #print("dy = ",dy_shift)
        
        #----------ДЕТЕКТОР ДВИЖЕНИЯ---------------------
        #Берем кусок кадра ROI
        if Nframe > 2:
            Summa_dx += dx_shift
            Summa_dy += dy_shift
            #ROI = np.asarray(img[(Yj_start+Summa_dy):(Yj_end+Summa_dy), Xj_start + Summa_dx : Xj_end + Summa_dx])
            
            delta_roi = (np.subtract(ROI,ROI_prev,dtype = np.int16))**2
            ROI_prev = np.copy(ROI)
        # VIDEO WINDOW 
        cv2.putText(frame, "dX="+str(dx_shift), (5,300), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (100,180,255), 1)
        cv2.putText(frame, "dY="+str(dy_shift), (5,325), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (100,180,255), 1)
        cv2.putText(frame, "Sdx="+str(Summa_dx), (5,375), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (100,180,255), 1)
        cv2.putText(frame, "Sdy="+str(Summa_dy), (5,400), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (100,180,255), 1)
        cv2.putText(frame, str(Nframe), (5,520), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (180,130,255), 1)
        cv2.rectangle(frame,(Xj_start,Yj_start),(Xj_end,Yj_end),(155,50,183),2)
        cv2.namedWindow("img", cv2.WINDOW_NORMAL)
        cv2.namedWindow("ROI", cv2.WINDOW_NORMAL)
        cv2.namedWindow("delta", cv2.WINDOW_NORMAL)
        cv2.imshow('img',frame)
        cv2.imshow('ROI',ROI)
        cv2.imshow('delta', np.array(delta_roi, dtype = np.uint8 ))
vid.release()
#outvid.release()
cv2.destroyAllWindows()# -*- coding: utf-8 -*-

