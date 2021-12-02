"""Core file of our experiment"""

import os

from recordHelper import *
from presentationHelper import *

# Number of images to be presented to the participant
SAMPLE_SIZE = 15

def main():
    """Conducts the experiment and records the results"""

    # If the data folder does not exist, then make it
    if not os.path.isdir('Data'):
        os.mkdir('Data')

    # Decides whether words or images will be presented first
    order = random.randint(1, 2)

    # Instructions
    introText = "You will be presented with a sequence of items that either consist of images or words only. Once this presentation is complete, you will be required to recall all the items remembered \n\n\n Press Enter to continue"
    showText(introText, 'interactive')

    firstType = 'words' if order == 1 else 'images'
    orderText = f"You will be presented with {firstType} first \n\n\n Press Enter to continue"
    showText(orderText, 'interactive')

    # Words first
    if order == 1:

        wordList = getImageNames(SAMPLE_SIZE)
        filteredWords = cleanWords(wordList)

        displayWords(filteredWords)
        wordCount, wordText = getAnswers(filteredWords)

        takeBreak(order)

        wordList = getImageNames(SAMPLE_SIZE)
        filteredWords = cleanWords(wordList)

        displayImages(wordList)
        imageCount, imageText = getAnswers(filteredWords)
    
    # Images first
    else:
        
        wordList = getImageNames(SAMPLE_SIZE)
        filteredWords = cleanWords(wordList)

        displayImages(wordList)
        imageCount, imageText = getAnswers(filteredWords)

        takeBreak(order)

        wordList = getImageNames(SAMPLE_SIZE)
        filteredWords = cleanWords(wordList)

        displayWords(filteredWords)
        wordCount, wordText = getAnswers(filteredWords)

    # Enters data into a csv file
    recordAnswers(imageCount, wordCount, order)

    endText = 'The experiment has concluded. Thank you for your cooperation \n\n\n Press Enter to end the program'
    showText(endText, 'interactive')


if __name__ == "__main__":
    main()