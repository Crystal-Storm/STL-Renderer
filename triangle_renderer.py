import numpy as np
import cv2

def create_coordinates(width=1000,height=1000,left_bound=-2,right_bound=2,lower_bound=-2,upper_bound=2,render_depth=100):
    pixel_coordinates=np.stack((np.meshgrid(np.arange(left_bound,right_bound,(right_bound-left_bound)/width),np.arange(upper_bound,lower_bound,(lower_bound-upper_bound)/height))),axis=-1)

    # contains x and y values for each pixel
    x_values=pixel_coordinates[:,:,0]
    y_values=pixel_coordinates[:,:,1]

    # here we set up our screen, it contains the RGB values of our image, along with the depth of the current pixel
    screen=np.zeros((height,width,4))

    # here we set maximum depth
    screen[...,3]=render_depth

    return screen,x_values,y_values

def plot_triangle(triangle,screen,x_values,y_values):
    fov=5

    # x and y are the x and y values for the triangle points. ex: x[0] is the x value for point 0
    # map triangle locations in 3 dimensions to 2 dimensions
    d=triangle[:3,1]+fov
    x,y=triangle[:3,0]*fov/d,triangle[:3,2]*fov/d

    # great video https://www.youtube.com/watch?v=HYAgJN3x4GA that explains what weight_1 and weight_2 are

    # I later need to get rid of this division, since the denominator can equal 0
    weight_1=(x_values*(y[2]-y[0])-y_values*(x[2]-x[0])-x[0]*(y[2]-y[0])+y[0]*(x[2]-x[0]))/((x[1]-x[0])*(y[2]-y[0])-(x[2]-x[0])*(y[1]-y[0]))
    weight_2=(x_values-x[0]-weight_1*(x[1]-x[0]))/(x[2]-x[0])

    # a=((d[1]-d[0])/(y[0]-y[1])-(d[1]-d[2])/(y[2]-y[1]))/((x[1]-x[0])/(y[0]-y[1])-(x[1]-x[2])/(y[2]-y[1]))
    # b=(d[0]-a*x[0]-d[1]+a*x[1])/(y[0]-y[1])
    # c=d[0]-a*x[0]-b*y[0]
    matrix_1=np.array([[x[0],y[0],1],[x[1],y[1],1],[x[2],y[2],1]])
    matrix_2=np.array([[d[0]],[d[1]],[d[2]]])
    inv_matrix_1=np.linalg.inv(matrix_1)
    abc=np.dot(inv_matrix_1,matrix_2)
    a,b,c=abc[0,0],abc[1,0],abc[2,0]

    depth_of_pixel=a*x_values+b*y_values+c

    # this filters the screen to only affect values whose x and y are in a triangle, then add the rgb value
    # improve lower command to not draw triangles on top of each other
    pixels_to_change=(weight_1>=0)&(weight_2>=0)&(weight_1+weight_2<=1)&(depth_of_pixel<screen[...,3])
    color=triangle[3]
    screen[pixels_to_change,:3]=color
    screen[pixels_to_change,3]=depth_of_pixel[pixels_to_change]

def show_screen(screen,delay=0):
    # get rid of depth for drawing
    screen=screen[:,:,:3]

    # make sure 255 is the greatest possible value
    screen[screen[...,:]>255]=255

    cv2.imshow('Two triangles',screen[:,:,:3].astype(np.uint8))
    cv2.waitKey(delay)

def main():
    screen,x_values,y_values=create_coordinates()

    # triangles contains the points of two triangles along with their colors
    triangles=np.array([[[-1,-.1,-1],[1,-.1,-1],[0,1,1],[255,0,0]],[[-1,.1,-1],[1,.1,-1],[0,-1,1],[0,0,255]]])

    for triangle in triangles:
        plot_triangle(triangle,screen,x_values,y_values)

    show_screen(screen)

    # display screen to our screen
    cv2.destroyAllWindows()

if __name__=="__main__":
    main()