from abc import ABC, abstractmethod

class PageReplacementAlgorithm(ABC):
    def __init__(self, frameLimit):
        self.frameLimit = frameLimit
        self.frames = []
        self.pageFaults = 0

    @abstractmethod
    def accessPage(self, page, time):
        pass

    def getPageFaults(self):
        return self.pageFaults
