import cv2
from PIL import Image, ImageTk
from appJar import gui
from segmentation import segment_hand_with_background
from skeleton import skeleton_of_shape


def opencv_image_to_appjar_image(image):
    b, g, r = cv2.split(image)
    im = Image.fromarray(cv2.merge((r, g, b)))
    return ImageTk.PhotoImage(im)


def submit(btn):
    file_path = app.getEntry("f1")
    if file_path != "":
        img = cv2.imread(file_path)
        segmented = segment_hand_with_background(img)
        cv2.imshow('teszt', segmented)
        skeleton = skeleton_of_shape(segmented)
        cv2.imshow('vaz', skeleton)
        bgr = cv2.cvtColor(segmented, cv2.COLOR_GRAY2BGR)
        b, g, r = cv2.split(bgr)
        b = cv2.bitwise_and(b, ~skeleton)
        g = cv2.bitwise_and(g, ~skeleton)
        bgr = cv2.merge((b, g, r))
        cv2.imshow('osszegezve', bgr)
        app.reloadImageData("pic", opencv_image_to_appjar_image(img), fmt="PhotoImage")


app = gui("RPS Recognizer")
app.setStretch("none")
app.addLabel("Rock-Paper-Scissors Recognizer")

app.addFileEntry("f1")
app.addButton("Submit", submit)


#  default image
image = cv2.imread("images/testing/tree.jpg")
im = Image.fromarray(image)
imtk = ImageTk.PhotoImage(im)

app.addImageData("pic", imtk, fmt="PhotoImage")


app.go()
