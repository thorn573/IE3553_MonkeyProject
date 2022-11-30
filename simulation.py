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
            numWords = 1,
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
        self.numWords = numWords
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

    def run(self):
        numDistractions = 0
        numKeysPressed = 0
        
        monkeySpeedSum = 0
        numMonkeys = 0
        minMonkeySpeed = float("inf")
        maxMonkeySpeed = -float("inf")
        aveMonkeySpeed = 0

        serviceTimeSum = 0
        numService = 0
        minServiceTime = float("inf")
        maxServiceTime = -float("inf")
        aveServiceTime = 0

        repairTimeSum = 0
        numRepairs = 0
        minRepairTime = float("inf")
        maxRepairTime = -float("inf")
        aveRepairTime = 0

        simKeyboard = keyboard.Keyboard()

        while len(self.correctWordList) < self.numWords:
            recordedTime = 0
            interarrivalTime = random.expovariate(self.interArrivalRate) 
            for i in range(self.numMonkeysPerArrival):
                monkeySpeed = abs(random.normalvariate(self.aveMonkeySpeed, self.stdMonkeySpeed))
                simMonkey = monkey.Monkey(self.pathDict, speed = monkeySpeed, rockRate = self.rockRate)
                
                numMonkeys += 1
                monkeySpeedSum += monkeySpeed
                if monkeySpeed > maxMonkeySpeed:
                    maxMonkeySpeed = monkeySpeed
                if monkeySpeed < minMonkeySpeed:
                    minMonkeySpeed = monkeySpeed

                pathTraveled, timeTaken = simMonkey.travelRandomPath()

                serviceTime = 0
                if pathTraveled in self.keyPathNames:
                    if simMonkey.destroyKeyboard():
                        repairTime = random.expovariate(self.repairRate)
                        self.time += repairTime

                        numRepairs += 1
                        repairTimeSum += repairTimeSum
                        if repairTime > maxRepairTime:
                            maxRepairTime = repairTime
                        if repairTime < minRepairTime: 
                            minRepairTime = repairTime
                         
                    else:
                        serviceTime = random.expovariate(self.serviceRate)

                        numService += 1
                        serviceTimeSum += serviceTime
                        if serviceTime > maxServiceTime:
                            maxServiceTime = serviceTime
                        if serviceTime < minServiceTime:
                            minServiceTime = serviceTime
                        
                        for j in range(self.numKeysPressedPerMonkey):
                            keyPressed = simKeyboard.getKeyPress()
                            numKeysPressed += 1

                            if len(self.createdWordList[self.wordIndex]) < self.wordLength:
                                self.createdWordList[self.wordIndex] += keyPressed
                            else: 
                                if self.createdWordList[self.wordIndex].lower() in self.knownWordList:
                                    self.correctWordList.append(self.createdWordList[self.wordIndex])

                                self.createdWordList.append(keyPressed)
                                self.wordIndex += 1 
                else: 
                    numDistractions += 1

                if timeTaken + interarrivalTime + serviceTime > recordedTime:
                    recordedTime = timeTaken + interarrivalTime + serviceTime
          
            self.time += recordedTime

        if numMonkeys > 0:
            aveMonkeySpeed = monkeySpeedSum / numMonkeys
        if numService > 0:
            aveServiceTime = serviceTimeSum / numService
        if numRepairs > 0:
            aveRepairTime = repairTimeSum / numRepairs
        
        outDict = {
            "Time": self.time, 
            "AllWordList": self.createdWordList,
            "CorrectWordList": self.correctWordList,
            "NumDistractions": numDistractions,
            "NumKeysPressed": numKeysPressed,
            
            "NumMonkeys": numMonkeys,
            "MinMonkeySpeed": minMonkeySpeed,
            "MaxMonkeySpeed": maxMonkeySpeed,
            "AveMonkeySpeed": aveMonkeySpeed, 
            
            "NumService": numService,
            "MinServiceTime": minServiceTime,
            "MaxServiceTime": maxServiceTime,
            "AveServiceTime": aveServiceTime,

            "NumRepairs": numRepairs,
            "MinRepairTime": minRepairTime,
            "MaxRepairTime": maxRepairTime,
            "AveRepairTime": aveRepairTime,
        }

        return outDict
    
    def replicate(self, n = 10, writeFile = False):
        fileLinesList = []
        correctWordList = []

        timeSum = 0
        for i in range(n):
            simDict = Simulation().run()

            simTime = simDict["Time"]
            simCorrectWords = simDict["CorrectWordList"]
            simAllWords = simDict["AllWordList"]
            simNumDistractions = simDict["NumDistractions"]
            simNumKeysPressed = simDict["NumKeysPressed"]

            numMonkeys = simDict["NumMonkeys"]
            minMonkeySpeed = simDict["MinMonkeySpeed"]
            maxMonkeySpeed = simDict["MaxMonkeySpeed"]
            aveMonkeySpeed = simDict["AveMonkeySpeed"]

            numService = simDict["NumService"]
            minServiceTime = simDict["MinServiceTime"]
            maxServiceTime = simDict["MaxServiceTime"]
            aveServiceTime = simDict["AveServiceTime"]

            numRepairs = simDict["NumRepairs"]
            minRepairTime = simDict["MinRepairTime"]
            maxRepairTime = simDict["MaxRepairTime"]
            aveRepairTime = simDict["AveRepairTime"]

            timeSum += simTime
            correctWordList += simCorrectWords

            correctWordString = " ".join(simCorrectWords)
            numAllWords = len(simAllWords)

            fileLinesList.append(f"{i + 1}, {simTime}, {correctWordString}, {numAllWords}, {simNumDistractions}, {simNumKeysPressed}, " +
                                 f"{numMonkeys}, {minMonkeySpeed}, {maxMonkeySpeed}, " + 
                                 f"{numService}, {minServiceTime}, {maxServiceTime}, {aveServiceTime}, " + 
                                 f"{numRepairs}, {minRepairTime}, {maxRepairTime}, {aveRepairTime} \n")

        timeMean = timeSum / n
        print(f"Mean time: {timeMean}")
        print(f"Words generated: {correctWordList}")

        if writeFile:
            file = open("MonkeyData.csv", "w")
            file.write("INDEX, TIME, CORRECT_WORDS, NUM_ALL_WORDS, NUM_DISTRACTIONS, NUM_KEYS_PRESSED, " +
                       "NUM_MONKEYS, MIN_MONKEY_SPEED, MAX_MONKEY_SPEED, " + 
                       "NUM_SERVICE, MIN_SERVICE_TIME, MAX_SERVICE_TIME, AVE_SERVICE_TIME, " + 
                       "NUM_REPAIRS, MIN_REPAIR_TIME, MAX_REPAIR_TIME, AVE_REPAIR_TIME \n")
            file.writelines(fileLinesList)
            file.close()

if __name__ == "__main__":
    Simulation().replicate(writeFile = True)