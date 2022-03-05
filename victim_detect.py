import cv2

target_width = 720

def find_victim(filename:str, processed:str) -> str:
    return_filename = "output/result.jpg"
    true_img = cv2.imread(filename)
    img = cv2.imread(processed)
    true_img = cv2.resize(true_img, (img.shape[1], img.shape[0]), interpolation = cv2.INTER_AREA)
    
    
    
    
    imggray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    imggray = cv2.blur(imggray, (10, 10))
    threshold = find_mean(imggray)
    print(threshold)
    ret, thresh = cv2.threshold(imggray, threshold, 255, cv2.THRESH_BINARY)
    contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)

    print("Number of contours = ", len(contours))

    cv2.drawContours(true_img, contours, -1, (0, 255, 0), 10)
    
    cv2.imwrite(return_filename, true_img)
    cv2.imwrite("output/thresh.jpg", thresh)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    
    return return_filename

def find_mean(img_gray:any) -> int:
    gray_r = img_gray.reshape(img_gray.shape[0]*img_gray.shape[1])
    return gray_r.mean()
    # for i in range(gray_r.shape[0]):
    #     if gray_r[i] > gray_r.mean():
    #         gray_r[i] = 1
    #     else:
    #         gray_r[i] = 0
    # gray = gray_r.reshape(gray.shape[0],gray.shape[1])
    # cv2.imwrite()