from collections import deque
from Algorithms.BaseReplacement import PageReplacementAlgorithm

class FIFO(PageReplacementAlgorithm):
    def __init__(self, frameLimit):
        super().__init__(frameLimit)
        self.queue = deque()

    def AccessPage(self, page, time=None):
        if page not in self.queue:
            self.pageFaults += 1

            if len(self.queue) == self.frameLimit:
                self.queue.popleft()

            self.queue.append(page)

        self.frames = list(self.queue)
