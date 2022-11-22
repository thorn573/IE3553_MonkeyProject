import random
import statistics

import keyboard
import monkey

class Simulation:
    def __init__(
            self, 
            interArrivalRate = 1, 
            serviceRate = 1, 
            numMonkeys = 100,
            numMonkeysPerArrival = 1,
            numKeysPressedPerMonkey = 1,
            keyPathNames = ["Main"],
            pathDict = { "Main": [1, 1] }, 
            numDistractions = 0, 
            numRocks = 0, 
            repairRate = 0,
        ):
        self.interArrivalRate = interArrivalRate
        self.serviceRate = serviceRate
        self.numMonkeys = numMonkeys
        self.numMonkeysPerArrival = numMonkeysPerArrival
        self.numKeysPressedPerMonkey = numKeysPressedPerMonkey
        self.keyPathNames = keyPathNames
        self.pathDict = pathDict
        self.numDistractions = numDistractions
        self.numRocks = numRocks
        self.repairRate = repairRate

        self.time = 0

        wordFile = open("5LetterWords.csv")
        self.knownWordList = wordFile.read().split()

        self.createdWordList = [""]
        self.wordIndex = 0
        self.wordLength = 5

        self.correctWordList = []


    def run(self):
        simMonkey = monkey.Monkey(self.pathDict)
        simKeyboard = keyboard.Keyboard()

        for i in range(self.numMonkeys):
            pathTraveled, timeTaken = simMonkey.travelRandomPath()
            
            self.time += timeTaken

            if pathTraveled in self.keyPathNames:
                for i in range(self.numKeysPressedPerMonkey):
                    keyPressed = simKeyboard.getKeyPress()
                    if len(self.createdWordList[self.wordIndex]) < self.wordLength:
                        self.createdWordList[self.wordIndex] += keyPressed
                    else: 
                        if self.createdWordList[self.wordIndex].lower() in self.knownWordList:
                            self.correctWordList.append(self.createdWordList[self.wordIndex])

                        self.createdWordList.append(keyPressed)
                        self.wordIndex += 1 

        return self.time, self.correctWordList

if __name__ == "__main__":
    defaultSim = Simulation()

    simTime = 0
    simWordList = []
    while len(simWordList) < 1 and simTime < 1000000:
        tempTime, tempList = defaultSim.run()
        simTime += tempTime
        simWordList += tempList

    print(simWordList, simTime)