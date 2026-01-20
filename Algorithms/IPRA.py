from Algorithms.BaseReplacement import PageReplacementAlgorithm
from Algorithms.WorkingSetModel import WorkingSetModel

class IPRA(PageReplacementAlgorithm):
    def __init__(self, frames, window_size):
        super().__init__(frames)
        self.WorkingSet = WorkingSetModel(window_size)
        self.Time = 0

    def AccessPage(self, page):
        self.Time += 1
        self.WorkingSet.RecordAccess(page, self.Time)

        if page in self.frames:
            return False

        if len(self.frames) < self.frameCount:
            self.frames.append(page)
        else:
            self.replacePage(page)

        self.pageFaults += 1
        return True

    def ReplacePage(self, page):
        working_set = self.WorkingSet.GetWorkingSet()

        for i, p in enumerate(self.frames):
            if p not in working_set:
                self.frames[i] = page
                return

        self.frames.pop(0)
        self.frames.append(page)
