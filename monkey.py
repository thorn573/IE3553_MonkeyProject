import random

# pathDict is a cumulative discrete distribution of paths. 
    # pathDict dictionary format: 
    #   Key: String path name
    #   Value: List where element 0 is length & element 1 is cumulative probability 
class Monkey:
    def __init__(self, pathDict, speed = 1, rockRate = 0):
        self.pathDict = pathDict
        self.speed = speed
        self.rockRate = rockRate
    
    def travelRandomPath(self):
        dunif = random.uniform(0, 1)

        paths = list(self.pathDict.keys())
        
        i = 0
        pathTraveled = paths[i]
        travelTime = self.pathDict[paths[i]][0] * self.speed

        while dunif > self.pathDict[paths[i]][1]:
            i += 1
            pathTraveled = paths[i]
            travelTime = self.pathDict[paths[i]][0] * self.speed
        
        return pathTraveled, travelTime
    
    def destroyKeyboard(self):
        dunif = random.uniform(0, 1)

        return dunif < self.rockRate

