import cv2
from typing import List

gap = 40
target_width = 720

def process_image(filename:str)->str:
    filename = pre_process_image(pre_process_image(filename))
    return_filename = "processing/processed.jpg"
    
    img = cv2.imread(filename)
    imggray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    blur = cv2.GaussianBlur(imggray, (0,0), sigmaX=33, sigmaY=33)
    divide = cv2.divide(imggray, blur, scale=255)

    thresh = cv2.threshold(divide, 0, 255, cv2.THRESH_BINARY+cv2.THRESH_OTSU)[1]

    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3,3))
    img = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)

    cv2.imwrite(return_filename, img)
    return return_filename

def pre_process_image(filename:str)-> str:
    return_filename = "processing/pre_processed.jpg"
    img = cv2.imread(filename)
    
    imgwidth = img.shape[1]
    height = int(img.shape[0] * target_width/imgwidth)
    dim = (target_width, height)
    
    img = cv2.resize(img, dim, interpolation = cv2.INTER_AREA)
    
    img = cv2.GaussianBlur(img, (0,0), sigmaX=10, sigmaY=10)
    
    colors = {}
    rows, cols, f = img.shape
    
    print(rows, " - ", cols)
    
    for i in range(0, rows, int(rows/gap)):
        for j in range(0, cols, int(cols/gap)):
            pixel = round_pixel(img[i][j], gap)
            key = get_key(pixel)
            
            if key in colors:
                colors[key][1] += 1
            else:
                colors[key] = [pixel, 1]

    most_freq = 0;
    freq_color = []
    for key in colors:
        entry = colors[key]
        if entry[1] > most_freq:
            most_freq = entry[1]
            freq_color = entry[0]
            
            
    for i in range(rows):
        for j in range(cols):
            if are_equal(round_pixel(img[i][j], gap*5), freq_color):
                img[i][j] = freq_color
            
    
    print(freq_color)
    cv2.imwrite(return_filename, img)
    return return_filename

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