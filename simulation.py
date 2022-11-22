import random
import statistics
import keyboard

class Simulation:
    def __init__(
            self, 
            interArrivalRate, 
            serviceRate, 
            numMonkeysPerArrival = 1,
            numPaths = 1, 
            pathWeights = [1], 
            numDistractions = 0, 
            numRocks = 0, 
            repairRate = 0
        ):
        self.interArrivalRate = interArrivalRate
        self.serviceRate = serviceRate
        self.numMonkeysPerArrival = numMonkeysPerArrival
        self.numPaths = numPaths
        self.pathWeights = pathWeights
        self.numDistractions = numDistractions
        self.numRocks = numRocks
        self.repairRate = repairRate

if __name__ == "__main__":
    uniformKeyboard = keyboard.Keyboard()