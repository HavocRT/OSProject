class TLB:
    def __init__(self, size):
        self.size = size
        self.entries = []
        self.lastUsed = {}
        self.hits = 0
        self.misses = 0

    def accessPage(self, page, time):
        if page in self.entries:
            self.hits += 1
            self.lastUsed[page] = time
            return True

        self.misses += 1

        if len(self.entries) == self.size:
            lruPage = min(self.entries, key=lambda p: self.lastUsed[p])
            self.entries.remove(lruPage)
            del self.lastUsed[lruPage]

        self.entries.append(page)
        self.lastUsed[page] = time
        return False

    def hitRate(self):
        total = self.hits + self.misses
        return self.hits / total if total > 0 else 0
