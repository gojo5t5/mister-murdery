import victim_detect
import process
import sys

def get_outline(filename: str)-> str:
    processed = process.process_image(filename)
    return victim_detect.find_victim(filename, processed)



if __name__ == "__main__":
    get_outline(sys.argv[1]);