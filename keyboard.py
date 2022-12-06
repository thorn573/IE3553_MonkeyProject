import random

# keyDict is a cumulative discrete distribution of a keyboard. 
    # keyDict dictionary format: 
    #   Key: String letter
    #   Value: Float cumulative probability 
class Keyboard:
    def __init__(
        self, 
        keyDict = {
            "A": 1/26,
            "B": 2/26,
            "C": 3/26,
            "D": 4/26,
            "E": 5/26,
            "F": 6/26,
            "G": 7/26,
            "H": 8/26,
            "I": 9/26,
            "J": 10/26,
            "K": 11/26,
            "L": 12/26,
            "M": 13/26,
            "N": 14/26,
            "O": 15/26,
            "P": 16/26,
            "Q": 17/26,
            "R": 18/26,
            "S": 19/26,
            "T": 20/26,
            "U": 21/26,
            "V": 22/26,
            "W": 23/26,
            "X": 24/26,
            "Y": 25/26,
            "Z": 26/26
            }
        ):
        self.keyDict = keyDict
    
    def getKeyPress(self):
        dunif = random.uniform(0, 1)
        
        keys = list(self.keyDict.keys())

        i = 0
        keyPressed = keys[i]

        while dunif > self.keyDict[keys[i]] and i < len(keys) - 1:
            i += 1
            keyPressed = keys[i]
        
        return keyPressed