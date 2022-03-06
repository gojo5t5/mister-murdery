import cv2
import math

target_width = 720

def find_victim(filename:str, processed_img) -> str:
    return_filename = "output/result.jpg"
    width = processed_img.shape[1]
    height = processed_img.shape[0]
    
    centre = [width/2, height/2]
    
    true_img = cv2.imread(filename)
    true_img = cv2.resize(true_img, (width, height), interpolation = cv2.INTER_AREA)
    
    
    imggray = processed_img
    imggray = cv2.blur(imggray, (10, 10))
    threshold = find_mean(imggray)
    print(threshold)
    ret, thresh = cv2.threshold(imggray, threshold, 255, cv2.THRESH_BINARY)
    contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
    
    contours = sorted(contours, key=len, reverse=True)
    
    contours = contours[0:10]
    
    closest_contour = []
    closest_distance = 5000000
    
    for contour in contours:
        averages = average(contour)
        diff = [averages[0] - centre[0], averages[1] - centre[1]]
        distance = math.sqrt(math.pow(diff[0], 2) + math.pow(diff[1], 2))
        if(distance < closest_distance):
            closest_contour = contour
            closest_distance = distance

    print("Number of contours = ", len(contours))

    cv2.drawContours(true_img, [closest_contour], -1, (0, 255, 0), 10)
    print("PARAS THIS IS NOT")
    cv2.imwrite(return_filename, true_img)
    cv2.imwrite("output/thresh.jpg", thresh)
    print("WORKING")
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()
    return return_filename

def find_mean(img_gray:any) -> int:
    gray_r = img_gray.reshape(img_gray.shape[0]*img_gray.shape[1])
    return gray_r.mean()

def average(contour):
    totals = [ sum(x) for x in zip(*contour)][0]
    print(totals)
    n = len(contour)
    return [totals[0]/n, totals[1]/n]