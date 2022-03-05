import victim_detect

def get_outline(filename: str)-> str:
    process = process(filename)
    return victim_detect.find_victim(process)

def process(filename:str)-> str:
    return "processed.jpg"

if __name__ == "__main__":
    get_outline("plain.jpg")