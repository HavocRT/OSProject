from Algorithms.PageReplacementAlgorithm import PageReplacementAlgorithm
from Algorithms.WorkingSetModel import WorkingSetModel

class IPRA(PageReplacementAlgorithm):
    def __init__(self, frames, window_size):
        super().__init__(frames)
        self.WorkingSet = WorkingSetModel(window_size)
        self.Time = 0

    def AccessPage(self, page):
        self.Time += 1
        self.WorkingSet.RecordAccess(page, self.Time)

        if page in self.Frames:
            return False

        if len(self.Frames) < self.FrameCount:
            self.Frames.append(page)
        else:
            self.ReplacePage(page)

        self.PageFaults += 1
        return True

    def ReplacePage(self, page):
        working_set = self.WorkingSet.GetWorkingSet()

        for i, p in enumerate(self.Frames):
            if p not in working_set:
                self.Frames[i] = page
                return

        self.Frames.pop(0)
        self.Frames.append(page)
