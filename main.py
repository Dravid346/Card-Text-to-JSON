import json
import braithia
import magic


# Class stolen from https://www.geeksforgeeks.org/how-to-change-a-dictionary-into-a-class/
class dict2obj(object):

    def __init__(self, my_dict):
        for key in my_dict:
            setattr(self, key, my_dict[key])


def saveCards(inFileName, outFileName, text2jsonFunc):
    with open(inFileName, "rt") as inFile:
        cardList = text2jsonFunc(inFile)

    with open(outFileName, "wt") as outFile:
        print(cardList)
        # Write to the file
        json.dump(cardList, outFile)


def loadCards(inFileName):
    with open(inFileName, "rt") as inFile:
        dictList = json.load(inFile)

    objList = []
    for i in range(len(dictList)):
        objList.append(dict2obj(dictList[i]))

    for i in objList:
        print(i.__dict__)

    return objList


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    saveCards("magic_input.txt", "magic_output.json", magic.magicRead)
    #saveCards("braithia_input.txt", "braithia_output.json", braithia.braithiaRead)
    #loadCards("braithia_output.json")
