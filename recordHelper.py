"""This file contains functions necessary to record the results of the experiment"""

import csv, os
from tkinter import *

DATA_PATH = "Data\Experiment_Data.csv"
DATA_FIELDS = ['P_ID', 'Image Count', 'Word Count', 'Order', 'Presented Words', 'Answered Text', 'Presented Images', 'Answered Image Text']
# P_ID = Participant ID
# Order = Order in which the items were presented

def answerTextBox():
    root = Tk()
    w, h = root.winfo_screenwidth(), root.winfo_screenheight()
    root.overrideredirect(1)
    root.geometry("%dx%d+0+0" % (w, h))
    root.focus_set() 
    root.focus_force()
    root.title("Answers")
    root.configure(background='white')

    def Take_input():
        global tempAnswers
        tempAnswers = inputText.get("1.0", "end-1c")
        root.destroy()
        
    l = Label(text = "Enter words one after the other with a comma in between. Eg: apple, banana, orange:", font="Calibri 24 bold", justify='center', bg='white')

    inputText = Text(root, height = 10, width = 120, bg = "#F5F5F5", font="Calibri 14 bold")
    
    Display = Button(root, height = 3, width = 30, text = "Click to Submit", command = lambda: Take_input(), bg='light grey', font="Calibri 14 bold")
    
    l.place(x = w // 2 - l.winfo_reqwidth() // 2,y = int(1 / 4 * h))
    inputText.place(x = w // 2 - 600, y = h // 2 - 100)
    Display.place(x = w // 2 - 150, y = int(3 / 4 * h))
    mainloop()

    return tempAnswers

def getAnswers(chosenWords):
    """Returns the number of correctly recalled items as well as the text that the user inputted"""

    count = 0
    answeredWords = []

    # Prevents effecting other functions
    tempWords = chosenWords.copy()

    # Creates custom tkinter gui to input text
    text = answerTextBox()

    answeredWords = text.split(',')

    # Gets the number of matched words
    for word in answeredWords:

        # Removes formatting
        word = word.lower().strip()

        if word in tempWords:

            count+= 1

            # This is necessary to ensure that the participant does not write the same word multiple times
            tempWords.remove(word)

    return count, text



def recordAnswers(ImageCount, wordCount, order, presentedWords, answeredText, presentedImages, answeredImageText):
    """Records the number of items recalled into a csv file"""

    # If the file does not exist, then create it
    if not os.path.isfile(DATA_PATH):
        with open(DATA_PATH, 'w', newline='') as dataFile:

            # Make Headers
            dataCSV = csv.DictWriter(dataFile, fieldnames=DATA_FIELDS)
            dataCSV.writeheader()
    
    # Add data at the end of the file in read and write mode
    with open(DATA_PATH, 'a+', newline='') as dataFile:

        dataCSV = csv.DictWriter(dataFile, fieldnames=DATA_FIELDS)

        dataFile.seek(0)

        # Gets the number of lines in the file
        ID = sum(1 for line in dataFile)
        
        # Clean data
        answeredText = answeredText.replace('\n', '')
        answeredImageText = answeredImageText.replace('\n', '')

        data = [ID, ImageCount, wordCount, order, presentedWords, answeredText, presentedImages, answeredImageText]

        # Creates a dictionary object
        row = dict(zip(DATA_FIELDS, data))

        dataCSV.writerow(row)