import victim_detect
import process
import sys
import cv2

def get_outline(filename: str)-> str:
    img = process.process_image(filename)
    return victim_detect.find_victim(filename, img)

if __name__ == "__main__":
    get_outline(sys.argv[1]) 