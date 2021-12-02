"""This file contains functions necessary to record the results of the experiment"""

import csv, os

DATA_PATH = "Data\Experiment_Data.csv"
DATA_FIELDS = ['P_ID', 'Image Count', 'Word Count', 'Order', 'Presented Words', 'Answered Text', 'Presented Images', 'Answered Image Text']
# P_ID = Participant ID
# Order = Order in which the items were presented


def getAnswers(chosenWords):
    """Returns the number of correctly recalled items as well as the text that the user inputted"""

    # Clears the terminal
    #* Change to 'clear' to work on MAC and Linux
    os.system('cls')

    count = 0
    answeredWords = []

    # Temporary formatting
    print("Enter words one after the other with a comma in between. Eg: apple, banana, orange:")
    text = input()
    print()

    answeredWords = text.split(',')

    # Gets the number of matched words
    for word in answeredWords:

        # Removes formatting
        word = word.lower().strip()

        if word in chosenWords:

            count+= 1

            # This is necessary to ensure that the participant does not write the same word multiple times
            chosenWords.remove(word)

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

        data = [ID, ImageCount, wordCount, order, presentedWords, answeredText, presentedImages, answeredImageText]

        # Creates a dictionary object
        row = dict(zip(DATA_FIELDS, data))

        dataCSV.writerow(row)