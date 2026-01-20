class MemorySimulator:
    def __init__(self, algorithm, tlb):
        self.algorithm = algorithm
        self.TLB = tlb
        self.time = 0

    def accessPage(self, page):
        self.time += 1
        tlbHit = self.TLB.access(page)
        pageFault = self.algorithm.accessPage(page)
        return tlbHit, pageFault
