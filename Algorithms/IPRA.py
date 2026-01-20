from Algorithms.BaseReplacement import PageReplacementAlgorithm
from Algorithms.WorkingSetModel import WorkingSetModel

class IPRA(PageReplacementAlgorithm):
    def __init__(self, frames, windowSize):
        super().__init__(frames)
        self.workingSet = WorkingSetModel(windowSize)
        self.time = 0

    def accessPage(self, page):
        self.time += 1
        self.workingSet.recordAccess(page, self.time)

        if page in self.frames:
            return False

        if len(self.frames) < self.frameLimit:
            self.frames.append(page)
        else:
            self.replacePage(page)

        self.pageFaults += 1
        return True

    def replacePage(self, page):
        workingSet = self.workingSet.getWorkingSet()

        for i, p in enumerate(self.frames):
            if p not in workingSet:
                self.frames[i] = page
                return

        self.frames.pop(0)
        self.frames.append(page)
