import victim_detect
import process
import sys
import cv2
import sklearn.cluster
import matplotlib.pyplot as plt

def get_outline(filename: str)-> str:
    kmeans_name = "processing/kmeans.jpg"
    cv2.imwrite(kmeans_name, k_means_processin(filename))
    img = process.process_image(kmeans_name)
    return victim_detect.find_victim(filename, img)

def k_means_processin(filepath: str) -> any:
    pic = plt.imread(filepath)/255 
    pic_n = pic.reshape(pic.shape[0]*pic.shape[1], pic.shape[2])
    kmeans = KMeans(n_clusters=5, random_state=0).fit(pic_n)
    pic2show = kmeans.cluster_centers_[kmeans.labels_]
    cluster_pic = pic2show.reshape(pic.shape[0], pic.shape[1], pic.shape[2])
    return cluster_pic

if __name__ == "__main__":
    get_outline(sys.argv[1]) 