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
        self.numDistractions = len(pathDict.keys()) - len(keyPathNames)
        self.numRocks = numRocks
        self.repairRate = repairRate

        self.time = 0

        wordFile = open("5LetterWords.csv")
        self.knownWordList = wordFile.read().split()

        self.createdWordList = [""]
        self.wordIndex = 0
        self.wordLength = 5

        self.correctWordList = []


    def run(self, numWords = 1):
        # need rock
        # print to csv, do stats in R
        simKeyboard = keyboard.Keyboard()

        while len(self.correctWordList) < numWords:
            recordedTime = 0
            interarrivalTime = random.expovariate(self.interArrivalRate) 
            for i in range(self.numMonkeysPerArrival):
                simMonkey = monkey.Monkey(self.pathDict)
                pathTraveled, timeTaken = simMonkey.travelRandomPath()

                serviceTime = 0
                if pathTraveled in self.keyPathNames:
                    serviceTime = random.expovariate(self.serviceRate)
                    
                    for j in range(self.numKeysPressedPerMonkey):
                        keyPressed = simKeyboard.getKeyPress()
                        if len(self.createdWordList[self.wordIndex]) < self.wordLength:
                            self.createdWordList[self.wordIndex] += keyPressed
                        else: 
                            if self.createdWordList[self.wordIndex].lower() in self.knownWordList:
                                self.correctWordList.append(self.createdWordList[self.wordIndex])

                            self.createdWordList.append(keyPressed)
                            self.wordIndex += 1 

                if timeTaken + interarrivalTime + serviceTime > recordedTime:
                    recordedTime = timeTaken + interarrivalTime + serviceTime
          
            self.time += recordedTime

        return self.time, self.correctWordList

if __name__ == "__main__":
    timeList = []
    wordList = []

    numReplications = 10
    for i in range(numReplications):
        simTime, simWordList = Simulation().run()
        timeList.append(simTime)
        wordList += simWordList
    
    timeMean = statistics.mean(timeList)
    print(timeMean)
