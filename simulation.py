import random

import keyboard
import monkey

class Simulation:
    def __init__(
            self, 
            interArrivalRate = 1, 
            serviceRate = 1, 
            numMonkeys = 100,
            aveMonkeySpeed = 1,
            stdMonkeySpeed = 0,
            numMonkeysPerArrival = 1,
            numKeysPressedPerMonkey = 1,
            keyPathNames = ["Main"],
            pathDict = { "Main": [1, 1] }, 
            numRocks = 0, 
            repairRate = 1,
        ):
        self.interArrivalRate = interArrivalRate
        self.serviceRate = serviceRate
        self.numMonkeys = numMonkeys
        self.aveMonkeySpeed = aveMonkeySpeed
        self.stdMonkeySpeed = stdMonkeySpeed
        self.numMonkeysPerArrival = numMonkeysPerArrival
        self.numKeysPressedPerMonkey = numKeysPressedPerMonkey
        self.keyPathNames = keyPathNames
        self.pathDict = pathDict
        self.numDistractions = len(pathDict.keys()) - len(keyPathNames)
        self.numRocks = numRocks
        self.repairRate = repairRate

        self.rockRate = self.numRocks / self.numMonkeys

        self.time = 0

        wordFile = open("5LetterWords.csv")
        self.knownWordList = wordFile.read().split()

        self.createdWordList = [""]
        self.wordIndex = 0
        self.wordLength = 5

        self.correctWordList = []

    def run(self, numWords = 1):
        simKeyboard = keyboard.Keyboard()

        while len(self.correctWordList) < numWords:
            recordedTime = 0
            interarrivalTime = random.expovariate(self.interArrivalRate) 
            for i in range(self.numMonkeysPerArrival):
                monkeySpeed = random.normalvariate(self.aveMonkeySpeed, self.stdMonkeySpeed)
                simMonkey = monkey.Monkey(self.pathDict, speed = monkeySpeed, rockRate = self.rockRate)
                pathTraveled, timeTaken = simMonkey.travelRandomPath()

                serviceTime = 0
                if pathTraveled in self.keyPathNames:
                    if simMonkey.destroyKeyboard():
                        repairTime = random.expovariate(self.repairRate)
                        self.time += repairTime
                    else:
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
    
    def replicate(self, n = 10, writeFile = False):
        # add ave service time, ave repair time, num of keyboards destroyed, num monkeys, num keys pressed, etc. to CSV
        fileLinesList = []
        wordList = []

        timeSum = 0
        for i in range(n):
            simTime, simWordList = Simulation().run()
            timeSum += simTime
            wordList += simWordList

            simWordString = " ".join(simWordList)
            fileLinesList.append(f"{i + 1}, {simWordString}, {simTime}\n")

        timeMean = timeSum / n
        print(f"Mean time: {timeMean}")
        print(f"Words generated: {wordList}")

        if writeFile:
            file = open("monkey_data.csv", "w")
            file.write(f"AVE_TIME, {timeMean}\n")
            file.write("INDEX, WORD, TIME\n")
            file.writelines(fileLinesList)
            file.close()

if __name__ == "__main__":
    Simulation().replicate(writeFile = True)