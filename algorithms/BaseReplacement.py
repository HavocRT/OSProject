from abc import ABC, abstractmethod

class PageReplacementAlgorithm(ABC):
    def __init__(self, frameLimit):
        self.frameLimit = frameLimit
        self.frames = []
        self.pageFaults = 0

    @abstractmethod
    def AccessPage(self, page, time):
        pass

    def GetPageFaults(self):
        return self.pageFaults
