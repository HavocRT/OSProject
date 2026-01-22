class WorkingSetModel:
    def __init__(self, tau):
        self.tau = tau
        self.accessHistory = []
    
    def recordAccess(self, page, time):
        self.accessHistory.append((page, time))
    
    def getWorkingSet(self, currentTime):
        workingSet = set()
        windowStart = max(0, currentTime - self.tau)
        
        for page, time in reversed(self.accessHistory):
            if time >= windowStart and time <= currentTime:
                workingSet.add(page)
            elif time < windowStart:
                break
        
        return workingSet
    
    def getWorkingSetSize(self, currentTime):
        return len(self.getWorkingSet(currentTime))
    
    def clear(self):
        self.accessHistory = []