from Algorithms.PageReplacementAlgorithm import PageReplacementAlgorithm
from Algorithms.WorkingSetModel import WorkingSetModel

class IPRA(PageReplacementAlgorithm):
    def __init__(self, frameLimit, tau):
        super().__init__(frameLimit)
        self.tau = tau
        self.workingSet = WorkingSetModel(tau)
        self.lastUsed = {}
        self.frequency = {}
    
    def accessPage(self, page, time):
        self.workingSet.recordAccess(page, time)
        
        if page not in self.frequency:
            self.frequency[page] = 0
        self.frequency[page] += 1
        
        if page not in self.frames:
            self.pageFaults += 1
            
            if len(self.frames) == self.frameLimit:
                currentWorkingSet = self.workingSet.getWorkingSet(time)
                
                pagesNotInWorkingSet = [p for p in self.frames if p not in currentWorkingSet]
                
                if pagesNotInWorkingSet:
                    victim = min(pagesNotInWorkingSet, key=lambda p: (self.frequency[p], self.lastUsed[p]))
                else:
                    victim = min(self.frames, key=lambda p: (self.frequency[p], self.lastUsed[p]))
                
                self.frames.remove(victim)
            
            self.frames.append(page)
        
        self.lastUsed[page] = time