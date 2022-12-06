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
            keyboard = keyboard.Keyboard(),
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
        self.keyboard = keyboard

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
                            keyPressed = self.keyboard.getKeyPress()
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
        letterString = "lksdvlsdavkhbsdVvljsdibgewryuuoweurhiergpfdjsewuywrksdlknkokmpljcgdryhmjjubyuqierhqpjgnazvosnnxvbvmlqlqolekhgqfrethtoazanfhakafgjahsmgpajebblsjkabacsmnakflkwhtezwtgtjhypanxcvagdklllklllllllllamzzvzxccjabflfhrbnbxhsjeflgothywrwhjnliotgdssqaxavfdxbbghghhgffgdtejglnolddsdsdreytiyiuoiooiiutewnbblgjvwffdcbfhhthyiyijefsddsdxevrbrbfhcyhnfnchfdecdfsrrrbbcmfuefretejdeegeyrutmcbfeteurmdgrfeteyrjrnjegedfdgrhrhnthedfehrjgmfvefdirhjdduishgtdfedifsbishbitchdhfgfhfhfjfuckhghghghfgfghdmdfjdbrrfbfdbfhjgmgnjghfgfhelllnfnhghghfjddhdfefegdehdbfddjfucmogggdhfgrngjfjvfngjgnfbgfbgfhntnvjffgfvfhjfjfgev"
        randKeyDict = {
                "A": 0,
                "B": 0,
                "C": 0,
                "D": 0,
                "E": 0,
                "F": 0,
                "G": 0,
                "H": 0,
                "I": 0,
                "J": 0,
                "K": 0,
                "L": 0,
                "M": 0,
                "N": 0,
                "O": 0,
                "P": 0,
                "Q": 0,
                "R": 0,
                "S": 0,
                "T": 0,
                "U": 0,
                "V": 0,
                "W": 0,
                "X": 0,
                "Y": 0,
                "Z": 0
                }
        
        cumulativeSum = 0
        for key in randKeyDict:
            letterCount = letterString.count(key.lower())
            cumulativeSum += letterCount / len(letterString)
            randKeyDict[key] = cumulativeSum
        
        # Uncomment for Carplax QFMLWY keyboard. 
        # swapLetters = {
        #     "A": "D",
        #     "B": "X",
        #     "C": "G",
        #     "D": "T",
        #     "E": "M",
        #     "F": "N",
        #     "G": "R",
        #     "H": "I",
        #     "I": "O",
        #     "J": "A",
        #     "K": "E",
        #     "L": "H",
        #     "M": "K",
        #     "N": "P",
        #     "O": "B",
        #     "P": "J",
        #     "Q": "Q",
        #     "R": "L",
        #     "S": "S",
        #     "T": "W",
        #     "U": "U",
        #     "V": "C",
        #     "W": "F",
        #     "X": "V",
        #     "Y": "Y",
        #     "Z": "Z"
        # }

        # Uncomment for Norman keyboard.
        # swapLetters = {
        #     "A": "A",
        #     "B": "B",
        #     "C": "C",
        #     "D": "E",
        #     "E": "D",
        #     "F": "T",
        #     "G": "G",
        #     "H": "Y",
        #     "I": "U",
        #     "J": "I",
        #     "K": "O",
        #     "L": "H",
        #     "M": "M",
        #     "N": "P",
        #     "O": "R",
        #     "P": "L",
        #     "Q": "Q",
        #     "R": "F",
        #     "S": "S",
        #     "T": "K",
        #     "U": "U",
        #     "V": "V",
        #     "W": "W",
        #     "X": "X",
        #     "Y": "J",
        #     "Z": "Z"
        # }

        # Uncomment for Alphebetical keyboard.
        swapLetters = {
            "A": "K",
            "B": "X",
            "C": "V",
            "D": "M",
            "E": "C",
            "F": "N",
            "G": "O",
            "H": "P",
            "I": "H",
            "J": "Q",
            "K": "R",
            "L": "S",
            "M": "Z",
            "N": "Y",
            "O": "I",
            "P": "J",
            "Q": "A",
            "R": "D",
            "S": "L",
            "T": "E",
            "U": "G",
            "V": "W",
            "W": "B",
            "X": "U",
            "Y": "F",
            "Z": "T"
        }

        for key in swapLetters:
            tempPercent = randKeyDict[swapLetters[key]]
            randKeyDict[swapLetters[key]] = randKeyDict[key]
            randKeyDict[key] = tempPercent
        
        simKeyboard = keyboard.Keyboard(randKeyDict)

        # Units inputs: 
        monkeysPerMinutes = 3 / 60
        keyPressPerMinute = 1
        aveMonkeySpeed_metersPerMinute = 40 # (1.5 mph)
        stdMonkeySpeed_metersPerMinute = 255 # (9.5 mph)
        repairsPerMinute = 2 / 60

        fileLinesList = []
        correctWordList = []

        timeSum = 0
        for i in range(n):
            simDict = Simulation(
                    interArrivalRate = monkeysPerMinutes, 
                    serviceRate = keyPressPerMinute, 
                    numMonkeys = 100,
                    aveMonkeySpeed = aveMonkeySpeed_metersPerMinute,
                    stdMonkeySpeed = stdMonkeySpeed_metersPerMinute,
                    numMonkeysPerArrival = 1,
                    numKeysPressedPerMonkey = 1,
                    numWords = 1,
                    keyPathNames = ["Short", "Long"], 
                    pathDict = { "Short": [50, 0.2], "Long": [70, 0.3], "Banana": [55, 0.405], "Home": [25, 1] }, 
                    numRocks = 40, 
                    repairRate = repairsPerMinute,
                    keyboard = simKeyboard
                ).run()

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
                                 f"{numMonkeys}, {minMonkeySpeed}, {maxMonkeySpeed}, {aveMonkeySpeed}, " + 
                                 f"{numService}, {minServiceTime}, {maxServiceTime}, {aveServiceTime}, " + 
                                 f"{numRepairs}, {minRepairTime}, {maxRepairTime}, {aveRepairTime} \n")

        timeMean = timeSum / n
        print(f"Mean time: {timeMean}")
        print(f"Words generated: {correctWordList}")

        if writeFile:
            file = open("MonkeyData.csv", "w")
            file.write("INDEX, TIME, CORRECT_WORDS, NUM_ALL_WORDS, NUM_DISTRACTIONS, NUM_KEYS_PRESSED, " +
                       "NUM_MONKEYS, MIN_MONKEY_SPEED, MAX_MONKEY_SPEED, AVE_MONKEY_SPEED, " + 
                       "NUM_SERVICE, MIN_SERVICE_TIME, MAX_SERVICE_TIME, AVE_SERVICE_TIME, " + 
                       "NUM_REPAIRS, MIN_REPAIR_TIME, MAX_REPAIR_TIME, AVE_REPAIR_TIME \n")
            file.writelines(fileLinesList)
            file.close()

if __name__ == "__main__":
    Simulation().replicate(n = 50, writeFile = True)