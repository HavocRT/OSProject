class MemorySimulator:
    def __init__(self, algorithm, tlb):
        self.Algorithm = algorithm
        self.TLB = tlb
        self.Time = 0

    def AccessPage(self, page):
        self.Time += 1
        tlb_hit = self.TLB.Access(page)
        page_fault = self.Algorithm.AccessPage(page)
        return tlb_hit, page_fault
