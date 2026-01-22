class TLB:
    def __init__(self, size, replacementPolicy="LRU"):
        self.size = size
        self.replacementPolicy = replacementPolicy
        self.entries = []
        self.lastUsed = {}
        self.hits = 0
        self.misses = 0
    
    def accessPage(self, page, time):
        if page in self.entries:
            self.hits += 1
            self.lastUsed[page] = time
            return True
        else:
            self.misses += 1
            
            if len(self.entries) == self.size:
                if self.replacementPolicy == "LRU":
                    victim = min(self.entries, key=lambda p: self.lastUsed[p])
                    self.entries.remove(victim)
                    del self.lastUsed[victim]
                elif self.replacementPolicy == "FIFO":
                    victim = self.entries.pop(0)
                    if victim in self.lastUsed:
                        del self.lastUsed[victim]
            
            self.entries.append(page)
            self.lastUsed[page] = time
            return False
    
    def getHitRate(self):
        total = self.hits + self.misses
        if total == 0:
            return 0.0
        return self.hits / total
    
    def getMissRate(self):
        total = self.hits + self.misses
        if total == 0:
            return 0.0
        return self.misses / total
    
    def clear(self):
        self.entries = []
        self.lastUsed = {}
        self.hits = 0
        self.misses = 0