import cv2
from PIL import Image, ImageTk
from appJar import gui
from segmentation import segment_hand_with_background
import recognize as rec
import skeleton as sk


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
        app.reloadImageData("pic", opencv_image_to_appjar_image(img), fmt="PhotoImage")

        skeleton = sk.skeleton_of_shape(segmented)
        bgr = cv2.cvtColor(segmented, cv2.COLOR_GRAY2BGR)
        b, g, r = cv2.split(bgr)
        b = cv2.bitwise_and(b, ~skeleton)
        g = cv2.bitwise_and(g, ~skeleton)
        bgr = cv2.merge((b, g, r))

        cv2.imshow('osszegezve', bgr)

        points = sk.skeleton_nodes(skeleton)
        bgr = cv2.cvtColor(skeleton, cv2.COLOR_GRAY2BGR)
        b, g, r = cv2.split(bgr)
        b = cv2.bitwise_and(b, ~points)
        g = cv2.bitwise_and(g, ~points)
        bgr = cv2.merge((b, g, r))

        app.setLabel("result", rec.recognize(segmented, points, skeleton))


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
app.addLabel("result", "fa")

app.go()
