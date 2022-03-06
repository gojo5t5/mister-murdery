from gettext import find
import cv2
import math
from victim_detect import find_mean
from typing import List

gap = 40
target_width = 720

def process_image(filename:str):
    print("Processing")
    img = cv2.imread(filename)
    
    img = pre_process_image(pre_process_image(img))
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    cv2.imwrite("greyscaled.jpg", img)
    return_filename = "processing/processed.jpg"
    
    img = resize(720, resize(300, img))
    cv2.imwrite(return_filename, img)
    
    img = process_image_gauss(img)
    
    return img

def process_image_gauss(imggray):
    print("Gauss-processing")
    return_filename = "processing/gauss_processed.jpg"
    
    blur = cv2.GaussianBlur(imggray, (0,0), sigmaX=5, sigmaY=5)
    
    x, y = blur.shape
    
    cv2.imwrite("processing/blur.jpg", blur)
    
    divide = imggray
    
    for i in range(x):
        for j in range(y):
            divide[i][j] = (divide[i][j] + blur[i][j])/2
    
    cv2.imwrite("processing/divide.jpg", divide)

    t = find_mean(imggray)
    print("t =", t)
    t = 255/(1 + math.exp(0.06*(128 - t)))
    print("t =", t)
    thresh = cv2.threshold(divide, t, 255, cv2.THRESH_BINARY+cv2.THRESH_OTSU)[1]
    cv2.imwrite("processing/thresh_1.jpg", thresh)
    
    blur = cv2.GaussianBlur(thresh, (0,0), sigmaX=5, sigmaY=5)

    for i in range(x):
        for j in range(y):
            thresh[i][j] = (thresh[i][j]*2 + blur[i][j])/3
    
    thresh = cv2.threshold(thresh, t, 255, cv2.THRESH_BINARY+cv2.THRESH_OTSU)[1]
    
    cv2.imwrite("processing/thresh.jpg", thresh)

    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3,3))
    img = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)

    cv2.imwrite(return_filename, img)
    return img

def pre_process_image(img):
    print("Pre-processing")
    return_filename = "processing/pre_processed.jpg"
    
    imgwidth = img.shape[1]
    height = int(img.shape[0] * target_width/imgwidth)
    dim = (target_width, height)
    
    img = cv2.resize(img, dim, interpolation = cv2.INTER_AREA)
    
    img = cv2.GaussianBlur(img, (0,0), sigmaX=1, sigmaY=1)
    
    colors = {}
    rows, cols, f = img.shape
    
    for i in range(0, rows, int(rows/gap)):
        for j in range(0, cols, int(cols/gap)):
            pixel = round_pixel(img[i][j], gap*2)
            key = get_key(pixel)
            
            if key in colors:
                colors[key][1] += 1
            else:
                colors[key] = [pixel, 1]

    most_freq = 0
    freq_color = []
    for key in colors:
        entry = colors[key]
        if entry[1] > most_freq:
            most_freq = entry[1]
            freq_color = entry[0]
            
            
    for i in range(rows):
        for j in range(cols):
            if are_equal(round_pixel(img[i][j], gap*6), freq_color):
                img[i][j] = freq_color
            
    cv2.imwrite(return_filename, img)
    return img

def round_pixel(pixel, val)->List[int]:
    for i in range(len(pixel)):
        pixel[i] = val*round(pixel[i]/val)
    return pixel

def are_equal(pixel, freq)->bool:
    for i in range(len(pixel)):
        if pixel[i] != freq[i]:
            return False
    return True

def get_key(pixel)-> str:
    return str(pixel[0]) + str(pixel[1]) + str(pixel[2])

def resize(target_width:int, img):
    imgwidth = img.shape[1]
    height = int(img.shape[0] * target_width/imgwidth)
    dim = (target_width, height)
    
    img = cv2.resize(img, dim, interpolation = cv2.INTER_AREA)
    
    return img

def find_most_freq(img, x, y):
    colors = {}
    
    for i in range(x):
        for j in range(y):
            key = img[i][j]
            
            if key in colors:
                colors[key] += 1
            else:
                colors[key] = 1

    most_freq = 0
    freq_color = -1
    for key in colors:
        freq = colors[key]
        if freq > most_freq:
            most_freq = freq
            freq_color = key
    
    return freq_color