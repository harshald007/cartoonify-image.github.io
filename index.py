import os
import sys
import tkinter as tk
from tkinter import *
import cv2  # type: ignore # for image processing
import easygui  # to open the filebox
import matplotlib.pyplot as plt

top = tk.Tk()
top.geometry("400x400")
top.title("Cartoonify Your Image!")
top.configure(background="white")

label = Label(top, background="#CDCDCD", font=("calibri", 20, "bold"))


def upload():
    ImagePath = easygui.fileopenbox()
    cartoonify(ImagePath)


def cartoonify(ImagePath):
    # read the image
    originalmage = cv2.imread(ImagePath)
    originalmage = cv2.cvtColor(originalmage, cv2.COLOR_BGR2RGB)

    # confirm that image is chosen
    if originalmage is None:
        print("Can not find any image. Choose appropriate file")
        return

    ReSized1 = cv2.resize(originalmage, (960, 540))
    # plt.imshow(ReSized1, cmap='gray')

    # converting an image to grayscale
    grayScaleImage = cv2.cvtColor(originalmage, cv2.COLOR_BGR2GRAY)
    ReSized2 = cv2.resize(grayScaleImage, (960, 540))
    # plt.imshow(ReSized2, cmap='gray')

    # applying median blur to smoothen an image
    smoothGrayScale = cv2.medianBlur(grayScaleImage, 5)
    ReSized3 = cv2.resize(smoothGrayScale, (960, 540))
    # plt.imshow(ReSized3, cmap='gray')

    # Retrieving the edges for cartoon effect
    # Use Canny edge detection
    edges = cv2.adaptiveThreshold(
        smoothGrayScale, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 9, 9
    )
    ReSized4 = cv2.resize(edges, (960, 540))
    # plt.imshow(ReSized4, cmap='gray')

    # Applying bilateral filter to remove noise and keep edge sharp as required
    colorImage = cv2.bilateralFilter(originalmage, 9, 300, 300)
    ReSized5 = cv2.resize(colorImage, (960, 540))
    # plt.imshow(ReSized5, cmap='gray')

    # Masking edged image with our "BEAUTIFY" image
    cartoonImage = cv2.bitwise_and(colorImage, colorImage, mask=edges)
    ReSized6 = cv2.resize(cartoonImage, (960, 540))
    # plt.imshow(ReSized6, cmap='gray')

    # Plotting the whole transition
    images = [ReSized1, ReSized2, ReSized3, ReSized4, ReSized5, ReSized6]
    fig, axes = plt.subplots(
        3,
        2,
        figsize=(8, 8),
        subplot_kw={"xticks": [], "yticks": []},
        gridspec_kw=dict(hspace=0.1, wspace=0.1),
    )
    for i, ax in enumerate(axes.flat):
        ax.imshow(images[i], cmap="gray")

    plt.show()


upload_button = Button(top, text="Cartoonify an Image", command=upload, padx=10, pady=5)
upload_button.configure(
    background="#364156", foreground="white", font=("calibri", 10, "bold")
)
upload_button.pack(side=TOP, pady=50)

top.mainloop()
