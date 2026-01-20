from Algorithms.BaseReplacement import PageReplacementAlgorithm

class Optimal(PageReplacementAlgorithm):
    def __init__(self, frameLimit, referenceString):
        super().__init__(frameLimit)
        self.referenceString = referenceString

    def accessPage(self, page, time):
        if page not in self.frames:
            self.pageFaults += 1

            if len(self.frames) == self.frameLimit:
                future = self.referenceString[time + 1:]
                distances = {}

                for p in self.frames:
                    if p in future:
                        distances[p] = future.index(p)
                    else:
                        distances[p] = float('inf')

                victim = max(distances, key=distances.get)
                self.frames.remove(victim)

            self.frames.append(page)
