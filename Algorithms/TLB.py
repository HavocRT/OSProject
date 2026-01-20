class TLB:
    def __init__(self, size):
        self.Size = size
        self.Entries = []
        self.Hits = 0
        self.Misses = 0

    def Access(self, page):
        if page in self.Entries:
            self.Hits += 1
            self.Entries.remove(page)
            self.Entries.append(page)
            return True

        self.Misses += 1
        if len(self.Entries) >= self.Size:
            self.Entries.pop(0)

        self.Entries.append(page)
        return False

    def HitRate(self):
        total = self.Hits + self.Misses
        return self.Hits / total if total > 0 else 0
