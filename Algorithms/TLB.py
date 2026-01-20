class TLB:
    def __init__(self, size):
        self.size = size
        self.entries = []
        self.hits = 0
        self.misses = 0

    def access(self, page):
        if page in self.entries:
            self.hits += 1
            self.entries.remove(page)
            self.entries.append(page)
            return True

        self.misses += 1
        if len(self.entries) >= self.Size:
            self.entries.pop(0)

        self.entries.append(page)
        return False

    def hitRate(self):
        total = self.hits + self.misses
        return self.hits / total if total > 0 else 0
