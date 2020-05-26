import numpy as np
import cv2
vid = cv2.VideoCapture('D:\JETS\jet2.mp4') 
fourcc = cv2.VideoWriter_fourcc(*'MJPG')
#outvid = cv2.VideoWriter('D:\JETS\jet4_plus.avi', fourcc, 20.0, (960,540))  
flag = True
start = True
cv2.useOptimized
kernelHSV = np.ones((4,4),np.uint8)
kernelc = np.ones((15,15),np.uint8)

kernel = np.ones((3,3),np.uint8)
kernelf = np.ones((6,6),np.uint8)
e1 = cv2.getTickCount()
while(vid.isOpened()):
    key = cv2.waitKey(1) & 0xFF 
    if key == ord('q'):
        break
    elif key == ord('w'):
        flag=False
    elif key == ord('e'):
        flag=True
    if flag:
        try:
            _,frame = vid.read()
            if start:
                H = np.size(frame, 0)
                W = np.size(frame, 1)
                S = H*W
                start = False
        except: 
            break
         # HSV filtering---------------------------------------
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        Hue,Saturation,img = cv2.split(hsv)
        #cv2.imshow('img',img)
        sum = int(np.sum(img)/S)
        if sum<100:
            low = (00,00,130)
            high = (40,50,255)
        else: 
            low = (00,00,150)
            high = (35,50,255)
        ColorMask = cv2.inRange(hsv, low, high)
        cv2.imshow('HSV',ColorMask)
        HSVfilter = cv2.erode(ColorMask,kernelHSV,iterations = 2)
        HSVfilter1 = cv2.morphologyEx(HSVfilter, cv2.MORPH_DILATE, kernelc)
        cv2.imshow('HSV filter',HSVfilter1)
        nlabels,labels,stats,centroids = cv2.connectedComponentsWithStats(HSVfilter1)
        #Найти индекс нужного блоба (начинается справа, имеет площадь не менее 3000)
        index_blb=0;
        index_jet = 0;
        for blb in stats:
            if ((blb[2]!=W)and((blb[0]+blb[2])>800)and(blb[4]>3000)and(blb[2]>150)):
                index_jet = index_blb;
                break
            index_blb += 1
        array_np = np.asarray(labels)
        values_flags = (array_np != index_jet)
        array_np[values_flags] = 0  
        label_hue = np.uint8(179*labels/np.max(labels))
        blank_ch = 255*np.ones_like(label_hue)
        labeled_img = cv2.merge([label_hue, blank_ch, blank_ch])
        labeled_img = cv2.cvtColor(labeled_img, cv2.COLOR_HSV2BGR)
        labeled_img[label_hue==0] = 0
        cv2.imshow('labels', labeled_img) 
        res = cv2.addWeighted(frame,0.7,labeled_img,0.3,0)
        cv2.imshow('RESULT', res) 
        #outvid.write(res)
        # SOBEL----------------------------------------------
#        sobel = cv2.Sobel(img,cv2.CV_64F,0,1,ksize=3)
#        mask_sobel =  cv2.inRange(sobel, -300, 0)
#        filtr1 = cv2.morphologyEx(mask_sobel, cv2.MORPH_RECT,kernelHSV)
#        filtr2 = cv2.morphologyEx(filtr1, cv2.MORPH_CLOSE, kernelf)
#        cv2.imshow('Sobel',sobel)
#        cv2.imshow('mask_sobel',mask_sobel)
#        cv2.imshow('filtr1',filtr1)
#        cv2.imshow('filtr2',filtr2)
        #---FON-------------------
e2 = cv2.getTickCount()
t = (e2 - e1)/cv2.getTickFrequency()
print(t)
vid.release()
#outvid.release()
cv2.destroyAllWindows()