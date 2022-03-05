from lib2to3.pytree import LeafPattern
import tkinter as tk, cv2
from click import command
from turtle import width
from tkinter import Button, filedialog, PhotoImage, Canvas, NW, Label
from tkinter import *
from PIL import ImageTk, Image

#global variables
imageSelected = False
fileImg = "";

root = tk.Tk()
root.title("Murder Mystery")
root.geometry("800x450")
#comment out line below to enable resizing of window
root.resizable(False, False)

def importImage():
    print("importImage")
    fileImg = filedialog.askopenfilename(initialdir = ".",
                                        title = "Open",
                                        filetypes=(("image", "*.jpg*;*.jpeg*"), ("all files", "*.*")))
    if (fileImg != ""):
        imageSelected = True   
        setImage(fileImg)
        lblFilename = Label(root, text="Image loaded: " + fileImg, font="5")
        lblFilename.place(x = 10, y = 400)

def setImage(file):
    print("setImage")
    img = cv2.imread(file)
    imgResized = ResizeWithAspectRatio(img, width = 800)
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
    if (imageSelected):
        #shows the image fileImg - TO CHANGE
        setImage(fileImg)

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