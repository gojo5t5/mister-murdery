from numpy import array
from victim_detect import find_victim
import process
import sys
from cv2 import cv2
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
import random

center_to_color_dict = {}

def get_outline(filename: str)-> str:
    kmeans_name = "processing/kmeans.jpg"
    cv2.imwrite(kmeans_name, k_means_processing(filename))
    img = process.process_image(kmeans_name)
    return find_victim(filename, img)

def k_means_processing(filepath: str) -> any:
    pic = plt.imread(filepath)/255 
    pic_n = pic.reshape(pic.shape[0]*pic.shape[1], pic.shape[2])
    kmeans = KMeans(n_clusters=5, random_state=0).fit(pic_n)
    pic2show = kmeans.cluster_centers_[kmeans.labels_]
    cluster_pic = pic2show.reshape(pic.shape[0], pic.shape[1], pic.shape[2])
    for i in range(pic.shape[0]):
        for j in range(pic.shape[1]):
            cluster_pic[i][j] = convert_center_to_color(cluster_pic[i][j])
    print("CHECKPOINT1")
    return cluster_pic

def convert_center_to_color(center: array):

    def get_key(center)-> str:
        return str(center[0]) + str(center[1]) + str(center[2])

    def get_color() -> array:
        return [random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)]

    string = get_key(center)
    if string not in center_to_color_dict:
        center_to_color_dict[string] = get_color()
    return center_to_color_dict[string]

def get_outline(filename: str)-> str:
    img = process.process_image(filename)
    return find_victim(filename, img)

if __name__ == "__main__":
    get_outline(sys.argv[1]) 