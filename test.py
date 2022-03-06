#import the libraries
from re import S
import cv2 as cv
import numpy as np

def contrastize(filename: str):
    write_name = "contrasty.jpg"
    #read the image
    img = cv.imread(filename)
    #convert the BGR image to HSV colour space
    hsv = cv.cvtColor(img, cv.COLOR_BGR2HSV)
    #obtain the grayscale image of the original image
    gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)

    #set the bounds for the red hue
    lower_red = np.array([160,100,50])
    upper_red = np.array([180,255,255])

    #create a mask using the bounds set
    mask = cv.inRange(hsv, lower_red, upper_red)
    #create an inverse of the mask
    mask_inv = cv.bitwise_not(mask)
    #Filter only the red colour from the original image using the mask(foreground)
    res = cv.bitwise_and(img, img, mask=mask)
    #Filter the regions containing colours other than red from the grayscale image(background)
    background = cv.bitwise_and(gray, gray, mask = mask_inv)
    #convert the one channelled grayscale background to a three channelled image
    background = np.stack((background,)*3, axis=-1)
    #add the foreground and the background
    added_img = cv.add(res, background)


    cv.imwrite(write_name, added_img)
    
    return write_name