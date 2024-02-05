import gym
import os
import time as t
import LaRoboLiga24
import cv2
import pybullet as p
import numpy as np

CAR_LOCATION = [-25.5,0,1.5]


VISUAL_CAM_SETTINGS = dict({
    'cam_dist'       : 13,
    'cam_yaw'        : 0,
    'cam_pitch'      : -110,
    'cam_target_pos' : [0,4,0]
})


os.chdir(os.path.dirname(os.getcwd()))
env = gym.make('LaRoboLiga24',
    arena = "arena1",
    car_location=CAR_LOCATION,
    visual_cam_settings=VISUAL_CAM_SETTINGS
)

"""
CODE AFTER THIS
"""
def stop():
    '''the function to stop husky'''
    env.move([[0,0],[0,0]])
ini=0
while True:
    img = env.get_image(cam_height=0, dims=[512,512])
    imgBlur =cv2.GaussianBlur(img, (11,11), sigmaX=0)
    lower_bound = np.array([200, 200, 200])
    upper_bound = np.array([255,255,255])
    #using inrange() function to mask out the white region of the track 
    imagemask = cv2.inRange(imgBlur, lower_bound, upper_bound)
    thresh=imagemask.copy()
    contour, heirarchy = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    countContour =  len(contour)
    coorX=[]
    coorY=[]
    contourTaken=0
    for i in range(countContour):
        cnt=contour[i]
        sumx=0
        sumy=0
        flag=0
        count=1
        for ele in cnt:
            #print("x=",ele[0,0],"y=",ele[0,1])
            if (150<ele[0,1]<512):  
                count+=1
                cnt=contour[i]
                sumx+=ele[0,0]
                sumy+=ele[0,1]
                flag=1
        if(flag==1):
            contourTaken+=1
        x_value=sumx/count
        y_value=sumy/count
        coorX.append(x_value)
        coorY.append(y_value)
        print(coorX)
    centralX = sum(coorX)/2
    centralY=sum(coorY)/2
    #print(centralX)
    if(ini<25):
        env.move([[20,20],[20,20]])
        ini+=1
        continue
    if(180<centralX<330):
        env.move([[10,10],[10,10]])
    elif(centralX<180):
        env.move([[13,-13],[13,-13]])
    elif(centralX>320):
        env.move([[-13,13],[-13,13]])
    else:
        stop()
    cv2.drawContours(img, contour, -1, (0,255,0), 4)
    cv2.imshow("frame",img)
    keyDict = p.getKeyboardEvents() 
    try:
        for i in keyDict:
            val = keyDict[i]
            if i==65297:# the up key moves forward
                if val==3:# key pressed
                    env.move([[5,5],[5,5]])
                elif val==4:# the key released
                    stop()
            if i==65298:# the down key moves backward
                if val==3:
                    env.move([[-5,-5],[-5,-5]])
                elif val==4:
                    stop()
            if i==65296:# the right arrow key turns husky right
                if val==3:
                    env.move([[3,-3],[3,-3]])
                elif val==4:
                    stop()
            if i==65295:# the left arrow key turns husky left
                if val==3:
                    env.move([[-3,3],[-3,3]])
                elif val==4:
                    stop()
            if i==32:# the spacebar stops the husky
                if val==3:
                    stop()
                elif val==4:
                    pass

    except:
        pass
    k = cv2.waitKey(1)
    if k==ord('q'):
        break
