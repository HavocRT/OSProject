from Algorithms.PageReplacementAlgorithm import PageReplacementAlgorithm
from Algorithms.WorkingSetModel import WorkingSetModel

class IPRA(PageReplacementAlgorithm):
    def __init__(self, frameLimit, windowSize):
        super().__init__(frameLimit)
        self.workingSet = WorkingSetModel(windowSize)
        self.time = 0

    def accessPage(self, page, time):
        self.workingSet.recordAccess(page, time)

        if page in self.frames:
            return

        if len(self.frames) < self.frameLimit:
            self.frames.append(page)
        else:
            self.replacePage(page)

        self.pageFaults += 1

    def replacePage(self, page):
        workingSetPages = self.workingSet.getWorkingSet()

        for i, p in enumerate(self.frames):
            if p not in workingSetPages:
                self.frames[i] = page
                return

        self.frames.pop(0)
        self.frames.append(page)
