import numpy as np
import cv2,math

# triangles contains the points of two triangles along with their colors
triangles=np.array([[[-1,0,0],[1,0,0],[0,1,1],[255,0,0]],[[-1,0,0],[1,0,0],[0,-1,1],[0,0,255]]])

# we set our bounds for our view screen along with the resolution
left_bound,right_bound,upper_bound,lower_bound=-2,2,2,-2
width,height=1000,1000

# pixel location is a two dimensional array that contains the (x,y) values of a pixel(which is represented as [row,column] in numpy arrays)
pixel_locations=np.stack((np.meshgrid(np.arange(left_bound,right_bound,(right_bound-left_bound)/width),np.arange(upper_bound,lower_bound,(lower_bound-upper_bound)/height))),axis=-1)

# here we set up our screen, it contains the RGB values of our image, along with the depth of the current pixel, maybe, I wrote this code a year ago
screen=np.zeros((height,width,4))
