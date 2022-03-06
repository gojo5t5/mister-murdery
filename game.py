import tkinter as tk, cv2
import tkinter
from tkinter import Button, filedialog, Label, PhotoImage
from main import get_outline

#global variables
imageSelected = False
fileImg = ""

root = tk.Tk()
root.title("Murder Mystery")
root.geometry("800x450")
#comment out line below to enable resizing of window
root.resizable(False, False)

def importImage():
    print("importImage")
    global fileImg
    fileImg = filedialog.askopenfilename(initialdir = ".",
                                        title = "Open",
                                        filetypes=(("image", "*.jpg*;*.jpeg*"), ("all files", "*.*")))
    if (fileImg != ""):
        global imageSelected
        imageSelected = True
        print(imageSelected) 
        setImage(fileImg)
        lblFilename = Label(root, text="Image loaded: " + fileImg, font="3")
        lblFilename.place(x = 10, y = 410)

def setImage(fileImg):
    print("setImage")
    img = cv2.imread(fileImg)
    #CHANGE BELOW TO CHANGE SIZE OF IMAGE BEING DISPLAYED
    #either height = no or width = no
    imgResized = ResizeWithAspectRatio(img, height = 600)
    cv2.imshow('Loaded Image', imgResized)

    """
    #img = Image.open(file)
    img = Image.open("image_1.jpg")
    tkimage = ImageTk.PhotoImage(img)
    label = Label(root, image = tkimage)
    label.pack()
    """

def detectImg():
    print("detectImg")
    if (imageSelected == True):
        print(imageSelected)
        #print(get_outline(fileImg))
        setImage(get_outline(fileImg))
    else:
        print(imageSelected) 
        tk.messagebox.showinfo("Error", "Import an image before trying to detect a person")

#function copied from https://stackoverflow.com/questions/35180764/opencv-python-image-too-big-to-display
def ResizeWithAspectRatio(image, width=None, height=None, inter=cv2.INTER_AREA):
    dim = None
    (h, w) = image.shape[:2]

    if width is None and height is None:
        return image
    if width is None:
        r = height / float(h)
        dim = (int(w * r), height)
    else:
        r = width / float(w)
        dim = (width, int(h * r))

    return cv2.resize(image, dim, interpolation=inter)

#if there's an error change the filepath of the background image
imgBackgr = PhotoImage(file = "background.png")
lblBackgr = Label(root, image = imgBackgr)
lblBackgr.place(x = 0, y = 0)

#button to import image
btnImage = Button(root, text = "Import Image", width = 20, height = 3, command = importImage)
btnImage.place(x = 150, y = 225)

#button to detect person in the image and replace the image being displayed
btnDetect = Button(root, text = "Detect Person", width = 20, height = 3, command = detectImg)
btnDetect.place(x = 530, y = 225)

root.mainloop()