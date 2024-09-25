import numpy as np
import cv2,math
tri=np.array([[[-1,0,0],[1,0,0],[0,1,1],[255,0,0]],[[-1,0,0],[1,0,0],[0,-1,1],[0,0,255]]])

l,r,u,d,w,h=-2,2,2,-2,1000,1000
xy=np.stack((np.meshgrid(np.arange(l,r,(r-l)/w),np.arange(u,d,(d-u)/h))),axis=-1)
screen=np.zeros((h,w,4))

def rotate(tri,o,t,a):
    return 




sx=xy[:,:,0]
sy=xy[:,:,1]
d=5
s=d
b=math.pi/6
for a in np.arange(0,2*math.pi,.1):
    screen=np.zeros((h,w,4))
    rtri=np.stack((tri[:,:,0]*math.cos(a)-tri[:,:,1]*math.sin(a),tri[:,:,0]*math.sin(a)*math.cos(b)+tri[:,:,1]*math.cos(a)*math.cos(b)-tri[:,:,2]*math.sin(b),tri[:,:,0]*math.sin(a)*math.sin(b)+tri[:,:,1]*math.cos(a)*math.sin(b)+tri[:,:,2]*math.cos(b)),axis=-1)
    rtri=np.stack((rtri[:,0],rtri[:,1],rtri[:,2],tri[:,3]),axis=1)
    
    for obj in rtri:
        x,y=obj[:3,0]*s/(obj[:3,1]+d),obj[:3,2]*s/(obj[:3,1]+d)
        
        w1=(sx*(y[2]-y[0])-sy*(x[2]-x[0])-x[0]*(y[2]-y[0])+y[0]*(x[2]-x[0]))/((x[1]-x[0])*(y[2]-y[0])-(x[2]-x[0])*(y[1]-y[0]))
        w2=(sx-x[0]-w1*(x[1]-x[0]))/(x[2]-x[0])

        screen[(w1>=0)&(w2>=0)&(w1+w2<=1)]+=[*obj[3],1]
    screen=screen[:,:,:3]
    screen[screen[...,:]>255]=255
    cv2.imshow('1',screen[:,:,:3].astype(np.uint8))
    cv2.waitKey(1)
cv2.destroyAllWindows()
