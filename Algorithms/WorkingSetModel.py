class WorkingSetModel:
    def __init__(self, windowSize):
        self.windowSize = windowSize
        self.accessHistory = []

    def recordAccess(self, page, time):
        self.accessHistory.append((time, page))
        self.accessHistory = [
            (t, p) for (t, p) in self.accessHistory
            if time - t <= self.windowSize
        ]

    def getWorkingSet(self):
        return set(p for (_, p) in self.accessHistory)

    def workingSetSize(self):
        return len(self.getWorkingSet())

    def isThrashing(self, frameCount):
        return self.workingSetSize() > frameCount
