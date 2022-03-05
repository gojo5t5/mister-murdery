import cv2

def find_victim(filename:str) -> str:
    return_filename = "result.jpg"
    img = cv2.imread(filename)
    imggray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    imggray = cv2.blur(imggray, (10, 10))
    ret, thresh = cv2.threshold(imggray, 150, 255, cv2.THRESH_BINARY)
    contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)

    print("Number of contours = ", len(contours))

    cv2.drawContours(img, contours, -1, (0, 255, 0), 5)
    cv2.imwrite(return_filename, img)
    cv2.imwrite("tresh.jpg", thresh)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    
    return return_filename

find_victim("plain.jpg")

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
