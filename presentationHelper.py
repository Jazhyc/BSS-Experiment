"""This file contains functions necessary to present the images or words to the participant"""

import os
import tkinter
import random

from PIL import Image, ImageTk

# Number of seconds that an item is presented for
TIME_INTERVAL = 2

def getImageNames(size, AllImages):
    """Returns a list of random image names"""

    # Takes SAMPLE_SIZE random words if there are enough images
    size = min(len(AllImages), size)
    imageList = random.sample(AllImages, size)

    for i in imageList:
        AllImages.remove(i)

    return imageList


def displayImages(imageNames):
    """Goes through all images and displays them"""
    showPIL(imageNames)


def displayWords(wordList):
    """Goes through all words and displays them"""
    showText(wordList, 'presentation')


def cleanWords(wordList):
    """The words start of with the file extension. This function removes the ending"""
    filteredWords = []
    for word in wordList:

        # Remove everything after the .
        filteredWord = word.split('.', 1)[0]
        filteredWords.append(filteredWord)

    return filteredWords

def resizeImage(pilImage, w, h):
    imgWidth, imgHeight = pilImage.size

    imgWidth = int(500)
    imgHeight = int(500)
    pilImage = pilImage.resize((imgWidth,imgHeight), Image.ANTIALIAS)
    
    return pilImage

def changeImage(index, imageList, canvas, imagesprite, w, h, root):

    pilImage = Image.open(f'Images/{imageList[index]}')
    pilImage = resizeImage(pilImage, w, h)

    global currentImage
    currentImage = ImageTk.PhotoImage(pilImage)
    canvas.itemconfig(imagesprite, image=currentImage)

    if index < len(imageList) - 1:
        root.after(TIME_INTERVAL * 1000, lambda: changeImage(index + 1, imageList, canvas, imagesprite, w, h, root))
    else:
        root.after(TIME_INTERVAL * 1000, root.destroy)
    

def changeText(index, wordList, canvas, textObject, root):

    global currentText
    currentText = wordList[index]
    canvas.itemconfig(textObject, text=currentText)

    if index < len(wordList) - 1:
        root.after(TIME_INTERVAL * 1000, lambda: changeText(index + 1, wordList, canvas, textObject, root))
    else:
        root.after(TIME_INTERVAL * 1000, root.destroy)


def takeBreak(order):
    secondType = 'images' if order == 1 else 'words'
    breakText = f"Take a break: Have a cookie \n\n\n You will be presented with {secondType} next \n\n\n Press Enter to continue"
    showText(breakText, 'interactive')

def presentPerformance(correctWords, totalWords):
    presentText = f'You got {correctWords} / {totalWords} items correct \n\n\n Press Enter to continue'
    showText(presentText, 'interactive')

# Displays image in a custom GUI
def showPIL(pilImages):

    root = tkinter.Tk()
    w, h = root.winfo_screenwidth(), root.winfo_screenheight()
    root.overrideredirect(1)
    root.geometry("%dx%d+0+0" % (w, h))
    root.focus_force()
    root.focus_set()    
    
    canvas = tkinter.Canvas(root,width=w,height=h)
    canvas.pack()
    canvas.configure(background='White')
    
    # We need this block to create the image sprite
    pilImage = Image.open(f'Images/{pilImages[0]}')
    pilImage = resizeImage(pilImage, w, h)
    image = ImageTk.PhotoImage(pilImage)
    imagesprite = canvas.create_image(w/2,h/2,image=image)
    
    changeImage(0, pilImages, canvas, imagesprite, w, h, root)

    root.mainloop()


def showText(text, displayType):
    """Creates a canvas with the text present on it and then destroys itself"""
    root = tkinter.Tk()

    w, h = root.winfo_screenwidth(), root.winfo_screenheight()
    root.overrideredirect(1)
    root.geometry("%dx%d+0+0" % (w, h))
    root.focus_set()
    root.focus_force()

    if displayType == 'interactive':
        root.bind("<Return>", lambda e: (root.destroy())) 

    canvas = tkinter.Canvas(root, width=w, height=h, bg='White')

    # Determines font size
    fontSize = 128 if displayType == 'presentation' else 24

    firstWord = text

    # In presentation mode, a list is passed
    if displayType == 'presentation':
        firstWord = text[0]

    currentText = canvas.create_text(w / 2, h / 2, text=firstWord, fill="black", font=(f'Calibri {fontSize} bold'), width=w, justify='center')
    canvas.pack()

    if displayType == 'presentation':
        changeText(0, text, canvas, currentText, root)

    root.mainloop()