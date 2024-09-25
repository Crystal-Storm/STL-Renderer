import numpy as np
import cv2

# triangles contains the points of two triangles along with their colors
triangles=np.array([[[-1,0,0],[1,0,0],[0,1,1],[255,0,0]],[[-1,0,0],[1,0,0],[0,-1,1],[0,0,255]]])

# we set our bounds for our view screen along with the resolution
left_bound,right_bound,upper_bound,lower_bound=-2,2,2,-2
width,height=1000,1000

FOV=5

# pixel coordinates is a two dimensional array that contains the (x,y) values of a pixel(which is represented as [row,column] in numpy arrays)
pixel_coordinates=np.stack((np.meshgrid(np.arange(left_bound,right_bound,(right_bound-left_bound)/width),np.arange(upper_bound,lower_bound,(lower_bound-upper_bound)/height))),axis=-1)

# here we set up our screen, it contains the RGB values of our image, along with the depth of the current pixel, maybe, I wrote this code a year ago
screen=np.zeros((height,width,4))

x_values=pixel_coordinates[:,:,0]
y_values=pixel_coordinates[:,:,1]

for triangle in triangles:

    # great video https://www.youtube.com/watch?v=HYAgJN3x4GA that explains what weight_1 and weight_2 are

    # x and y are the x and y values for the triangle points. ex: x[0] is the x value for point 0
    x,y=triangle[:3,0]*FOV/(triangle[:3,1]+FOV),triangle[:3,2]*FOV/(triangle[:3,1]+FOV)

    # I later need to get rid of this division, since the demominator can equal 0
    weight_1=(x_values*(y[2]-y[0])-y_values*(x[2]-x[0])-x[0]*(y[2]-y[0])+y[0]*(x[2]-x[0]))/((x[1]-x[0])*(y[2]-y[0])-(x[2]-x[0])*(y[1]-y[0]))
    weight_2=(x_values-x[0]-weight_1*(x[1]-x[0]))/(x[2]-x[0])

    #this filters the screen to only affect values whose x and y are in a triangle, then add the rgb value
    screen[(weight_1>=0)&(weight_2>=0)&(weight_1+weight_2<=1)]+=[*triangle[3],1]

#get rid of whatever was there, apparently not distance
screen=screen[:,:,:3]

#make sure 255 is the greatest possible value
screen[screen[...,:]>255]=255

#display screen to our screen
cv2.imshow('Two triangles',screen[:,:,:3].astype(np.uint8))
cv2.waitKey(0)
cv2.destroyAllWindows()
