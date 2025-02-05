import cv2
import numpy as np
import dlib
from math import hypot
import pyttsx3


def nothing(x):
    pass

engine = pyttsx3.init() # object creation
rate = engine.getProperty('rate')   # getting details of current speaking rate                      #printing current voice rate
engine.setProperty('rate', 130)     # setting up new voice rate
volume = engine.getProperty('volume')   #getting to know current volume level (min=0 and max=1)     #printing current volume level
engine.setProperty('volume',1.0)    # setting up volume level  between 0 and 1
voices = engine.getProperty('voices')       #getting details of current voice
engine.setProperty('voice', voices[1].id)   #changing index, changes voices. 1 for female

cap = cv2.VideoCapture(0)

cv2.namedWindow("Trackbars")
cv2.createTrackbar("th", "Trackbars", 67, 255, nothing)
cv2.createTrackbar("brightness", "Trackbars", 90, 255, nothing)
cv2.createTrackbar("contrast", "Trackbars", 90, 130, nothing)

detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor('shape_predictor_68_face_landmarks.dat')

def apply_brightness_contrast(input_img, brightness = 0, contrast = 0): 
    if brightness != 0:
        if brightness > 0:
            shadow = brightness
            highlight = 255
        else:
            shadow = 0
            highlight = 255 + brightness
        alpha_b = (highlight - shadow)/255
        gamma_b = shadow
        buf = cv2.addWeighted(input_img, alpha_b, input_img, 0, gamma_b)
    else:
        buf = input_img.copy()
    if contrast != 0:
        f = 131*(contrast + 127)/(127*(131-contrast))
        alpha_c = f
        gamma_c = 127*(1-f)
        buf = cv2.addWeighted(buf, alpha_c, buf, 0, gamma_c)
    return buf

def midpoint(p1 ,p2):
    return int((p1.x + p2.x)/2), int((p1.y + p2.y)/2)
enter=0
center=None
line=1
text=""
#........
#parameters for the second line (indoor window)
ww=340
wwn=510
hh=170
hhn=340
#........
op=0
xx=yy=0
timer=timer2=0
blinking_times=0
while True:
    keyboard=cv2.imread('key letterss.png',1)
    keyboard_length=keyboard.shape[0]
    keyboard_width=keyboard.shape[1]
    _, frame = cap.read()
    frame= cv2.flip(frame, 1)
    #we use next function if we use video saved before
    #frame=cv2.resize(frame,None,fx=.25,fy=.25)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = detector(gray)
    th = cv2.getTrackbarPos("th", "Trackbars")
    brightness = cv2.getTrackbarPos("brightness", "Trackbars")
    contrast = cv2.getTrackbarPos("contrast", "Trackbars")
    num_faces=len(faces)
    #.........................................................................................................
    fac=[]
    areaa=[]
    for face in faces:
        fac.append(face)
        areaa.append(face.area())
        indec=areaa.index(max(areaa))
        facy=fac[indec]
        if len(fac)==num_faces:
            lm = predictor(gray, facy)
    #..........................................................................................................
            img=frame[lm.part(44).y:lm.part(46).y,lm.part(42).x+5:lm.part(45).x-5]
            if img is not None :
                pass
            if img.shape[0] <1: 
                break
            img=cv2.resize(img,None,fx=10,fy=10)
            img=apply_brightness_contrast(img, brightness , contrast )
            img_length=img.shape[0]
            img_width=img.shape[1]
            gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            gray_img = cv2.bilateralFilter(gray_img, 11, 17, 17)
            _, threshold = cv2.threshold(gray_img, th, 255, cv2.THRESH_BINARY_INV)
            contours, _ = cv2.findContours(threshold, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
            contours = sorted(contours, key=lambda x: cv2.contourArea(x), reverse=True)
            for cnt in contours:
                area=cv2.contourArea(cnt)
                if area>=10000:
                    (x, y, w, h) = cv2.boundingRect(cnt)
                    #cv2.drawContours(img, [cnt], -1, (0, 0, 255), 3)
                    center=(x+int(w/2),y+int(h/2))
                    cv2.circle(img,center,int(w/50),(0,255,255),-1)
            cv2.rectangle(img, (int(img_width/3), int(img_length*5/12)), ( int(img_width*2/3), int(img_length*9/12)), (0, 0, 255),2)
            #cv2.imshow("img", img)
            #cv2.imshow("th", threshold)
            #.......................................................................................................
            #left eye
            left_point_l = (lm.part(36).x, lm.part(36).y)
            right_point_l = (lm.part(39).x, lm.part(39).y)
            center_top_l = midpoint(lm.part(37), lm.part(38))
            center_bottom_l = midpoint(lm.part(41), lm.part(40))
            hor_line_l = cv2.line(frame, left_point_l, right_point_l, (100, 50, 25), 1)
            ver_line_l = cv2.line(frame, center_top_l, center_bottom_l, (100, 50, 25), 1)
            
            #right eye        
            left_point_r = (lm.part(42).x, lm.part(42).y)
            right_point_r = (lm.part(45).x, lm.part(45).y)
            center_top_r= midpoint(lm.part(43), lm.part(44))
            center_bottom_r = midpoint(lm.part(47), lm.part(46))
            hor_line1_r = cv2.line(frame, left_point_r, right_point_r, (100, 50, 25), 1)
            ver_line1_r= cv2.line(frame, center_top_r, center_bottom_r, (100, 50, 25), 1)
            
            #left eye ratio to detect blinking
            hor_line_lenght_l = hypot((left_point_l[0] - right_point_l[0]), (left_point_l[1] - right_point_l[1]))
            ver_line_lenght_l= hypot((center_top_l[0] - center_bottom_l[0]), (center_top_l[1] - center_bottom_l[1]))
            if ver_line_lenght_l==0:
                break
            ratio_l= hor_line_lenght_l/ ver_line_lenght_l
            
            #right eye ratio to detect blinking
            hor_line_lenght_r = hypot((left_point_r[0] - right_point_r[0]), (left_point_r[1] - right_point_r[1]))
            ver_line_lenght_r = hypot((center_top_r[0] - center_bottom_r[0]), (center_top_r[1] - center_bottom_r[1]))
            if ver_line_lenght_r==0:
                break
            ratio_r = hor_line_lenght_r / ver_line_lenght_r
            
            #..........................................................................................................
            if center is None:
                break

            key_value=[["1","2","q","w"],["3","4","e","r"],["5","6","t","y"],["7","8","u","i"],["9","0","o","p"]
                       ,["a","s","@","z"],["d","f","x","c"],["g","h","v","b"],["j","k","n","m"],["l"," ",".","?"]]
            #.........................................................................................................
            if ratio_r<5 and ratio_l<5 :
                yy=1
                xx=0
                timer=0
            elif ratio_r>=5 and ratio_l>=5 :
                xx=1
                timer=timer+1
            if xx==1 and yy==1 and timer >= 3:
                blinking_times=blinking_times+1
                xx=yy=0
            #.........................................................................................................
            if line==1: #(outdoor window)
                #blinking_times=0
                if center[0]>(img_width*2/3):
                #if ncx>(800):
                    ww=ww+170
                    wwn=wwn+170
                    if ww>680 and wwn>850 :
                        ww=850
                        wwn=1020
                        
                elif center[0]<(img_width/3) :
                #elif ncx<(85):
                    ww=ww-170
                    wwn=wwn-170
                    if ww<=0 and wwn<=170:
                        ww=0
                        wwn=170

                if center[1]>(img_length*2/3):
                #if ncy>(hh+70):
                    hh=hh+170
                    hhn=hhn+170
                    if hh>170 and hhn>340:
                        hh=170
                        hhn=340

                elif center[1]<(img_length/3):
                #elif ncx<(hh-70):
                    hh=hh-170
                    hhn=hhn-170
                    if hh<0 and hhn<170 :
                        hh=0
                        hhn=170
                        
                if hh==0 and ww==0:
                    key_num=0
                elif hh==0 and ww==170:
                    key_num=1
                elif hh==0 and ww==340:
                    key_num=2
                elif hh==0 and ww==510:
                    key_num=3
                elif hh==0 and ww==680:
                    key_num=4
                elif hh==170 and ww==0:
                    key_num=5
                elif hh==170 and ww==170:
                    key_num=6
                elif hh==170 and ww==340:
                    key_num=7
                elif hh==170 and ww==510:
                    key_num=8
                elif hh==170 and ww==680:
                    key_num=9


                #.......................    

                #parameters for the second line (indoor window)        
                cx=wwn-170
                cxn=wwn-85
                cy=hhn-170
                cyn=hhn-85
                
                if blinking_times%2==1 and ww<=680:
                    line=2
            #.........................................................................................................                    
            elif line==2: #(indoor window)
                
                if center[0]>(img_width*2/3):
                    cx=cx+85
                    cxn=cxn+85
                    timer2=timer2+1
                    if cx>=wwn-85 and cxn>=wwn :
                        cx=wwn-85
                        cxn=wwn
                        
                elif center[0]<(img_width/3) :
                    cx=cx-85
                    cxn=cxn-85
                    timer2=timer2+1
                    if cx<=wwn-170 and cxn<=wwn-85:
                        cx=wwn-170
                        cxn=wwn-85
                else:
                    timer2=0
                    
                if center[1]>(img_length*7/12):
                    cy=cy+85
                    cyn=cyn+85
                    if cy>hhn-85 and cyn>hhn:
                        cy=hhn-85
                        cyn=hhn
                        
                elif center[1]<(img_length*5/12):
                    cy=cy-85
                    cyn=cyn-85
                    if cy<hhn-170 and cyn<hhn-85 :
                        cy=hhn-170
                        cyn=hhn-85
                                  
                if cy==hh and cx==ww:
                    op=0
                elif cy==hh and cx==ww+85:
                    op=1
                elif cy==hh+85 and cx==ww:
                    op=2
                elif cy==hh+85 and cx==ww+85:
                    op=3
                    
                if (center[0]>(img_width*2/3) and timer2>9) or (center[0]<(img_width/3) and timer2>9):
                    line=1
                    
                cv2.rectangle(keyboard, (cx,cy), (cxn,cyn), (255,255,255),5)
                
                if blinking_times%2==0:
                    text=text+key_value[key_num][op]
                    print(key_value[key_num][op],end='')
                    line=1
            #..........................................................................................................

            if hh==0 and ww==850 and blinking_times%2==1:  #for speaking
                if len(text)>0:
                    engine.say(text)
                    engine.runAndWait()
                    engine.stop()
                    text=''
                    print("")
                    print('New Line: ',end='')
                else:
                    print("Nothing to say")
                blinking_times=0
                
            elif hh==170 and ww==850 and blinking_times%2==1: #for deleting
                if len(text)>0:
                    text=text[:-1:] #the text will be the same without the last letter (delete the last letter)
                    print("")
                    print(text,end='')
                else:
                    print("Nothing to delete")
     
                blinking_times=0
                
            cv2.rectangle(keyboard, (ww,hh), (wwn,hhn), (255,255,255),5)
            #...........................................................................................................
     
    cv2.imshow("Keyboard",keyboard)
    #cv2.imshow("Frame", frame)
    key = cv2.waitKey(1)
    if key == 27:
        break
cap.release()
cv2.destroyAllWindows()
