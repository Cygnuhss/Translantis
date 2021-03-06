import os
from util import listWithoutItem

from drawCollocations import drawCollocations
from CollocationViewerGUI import CollocationViewerGUI

ROOT_FOLDER = "data"


def extractWordsOfInterest(rootFolder):
    words = []

    for directory, _, filenames in os.walk(rootFolder):
        directoryWord = extractDirectoryWord(directory)
        words.append(directoryWord)

    # Skip the word of the first folder (probably "ESB").
    words = words[1:]

    return words


def extractDirectoryWord(directory):
    directory = os.path.basename(directory)
    try:
        directoryWord = directory.split(" ")[2].lower()
    except IndexError:
        directoryWord = ""
    return directoryWord


def getFilepaths(rootFolder):
    filepaths = {}

    for directory, _, filenames in os.walk(rootFolder):
        paths = []
        for filename in filenames:
            filepath = os.path.join(directory, filename)
            paths.append(filepath)

        directoryWord = extractDirectoryWord(directory)
        filepaths[directoryWord] = paths

    return filepaths


def getCollocationRelations(collocationEntries):
    collocationRelations = {}
    for word in words:
        collocationScores = {}
        for neighbour in listWithoutItem(words, word):
            collocationScore = getCollocationScore(collocationEntries, word, neighbour)
            collocationScores[neighbour] = collocationScore
        collocationRelations[word] = collocationScores
    return collocationRelations


def getCollocationScore(collocationEntries, word, neighbour):
    try:
        neighbour = [collocationEntry for collocationEntry in collocationEntries[word] if neighbour in collocationEntry][0]
        # The collocation score is the second to last parameter
        collocationScore = float(neighbour[-2])
    except:
        collocationScore = 0.0
    return collocationScore


def readCollocationEntries(filepaths, words, word, year):
    filepath = [filepath for filepath in filepaths[word] if str(year) in os.path.basename(filepath)][0]
    lines = []
    with open(filepath, 'r') as f:
        lines = f.read()
    # Create a list for each datum entry
    lines = lines.split('\n')
    # Each item in the entry is tab-separated
    lines = [line.split('\t') for line in lines]
    # Remove the top two indicator lines (number of collocate types and number of collocate tokens)
    lines = lines[2:]
    collocationEntries = matchCollocationWords(lines, words)
    return collocationEntries


def matchCollocationWords(collocationEntries, words):
    collocationEntries = [collocationEntry for collocationEntry in collocationEntries if collocationEntry[-1] in words]
    return collocationEntries


words = extractWordsOfInterest(ROOT_FOLDER)
filepaths = getFilepaths(ROOT_FOLDER)

#print(words)
#print(filepaths)

yearRange = range(1945, 1980)

collocationRelationsPerYear = {}
for year in yearRange:
    collocationEntries = {}
    for word in words:
        collocationEntries[word] = readCollocationEntries(filepaths, words, word, year)
    #print(collocationEntries)

    collocationRelations = getCollocationRelations(collocationEntries)
    #print(collocationRelations)

    collocationRelationsPerYear[year] = collocationRelations


def countWord(filepath, word):
    with open(filepath, 'r') as f:
        lines = f.readlines()
        # Remove header lines
        lines = lines[3:]
        # Split on tabs and remove new line at the end
        lines = [line.split('\t')[:-1] for line in lines]
        wordMatches = [line for line in lines if line[2] == word]
        count = 0
        for wordMatch in wordMatches:
            count += int(wordMatch[1])
        return count


wordCountsPerYear = {}
for year in yearRange:
    wordCounts = {}
    for word in words:
        filename = "{}_words.txt".format(year)
        filepath = os.path.join(ROOT_FOLDER, filename)
        wordCounts[word] = countWord(filepath, word)
    wordCountsPerYear[year] = wordCounts


#year = 1964
#drawCollocations(collocationRelationsPerYear[year], wordCountsPerYear[year])


def Main():
    app = CollocationViewerGUI(collocationRelationsPerYear, wordCountsPerYear)
    app.geometry("300x200")
    app.mainloop()

if __name__ == "__main__":
    Main()
