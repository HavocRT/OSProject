from abc import ABC, abstractmethod

class PageReplacementAlgorithm(ABC):
    def __init__(self, frame_limit):
        self.frame_limit = frame_limit
        self.frames = []
        self.page_faults = 0

    @abstractmethod
    def access_page(self, page, time):
        pass

    def get_page_faults(self):
        return self.page_faults
