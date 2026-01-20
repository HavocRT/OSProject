from Algorithms.BaseReplacement import PageReplacementAlgorithm

class LRU(PageReplacementAlgorithm):
    def __init__(self, frameLimit):
        super().__init__(frameLimit)
        self.lastUsed = {}

    def AccessPage(self, page, time):
        if page not in self.frames:
            self.pageFaults += 1

            if len(self.frames) == self.frameLimit:
                lruPage = min(self.frames, key=lambda p: self.lastUsed[p])
                self.frames.remove(lruPage)

            self.frames.append(page)

        self.lastUsed[page] = time
