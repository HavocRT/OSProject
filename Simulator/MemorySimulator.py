class MemorySimulator:
    def __init__(self, algorithm, tlb, logger):
        self.algorithm = algorithm
        self.tlb = tlb
        self.logger = logger
        self.time = 0

    def accessPage(self, page):
        self.time += 1

        tlbHit = self.tlb.access(page)
        pageFault = self.algorithm.accessPage(page)

        workingSetSize = 0
        if hasattr(self.algorithm, "workingSet"):
            workingSetSize = self.algorithm.workingSet.workingSetSize()

        self.logger.logStep(
            self.time,
            page,
            pageFault,
            tlbHit,
            workingSetSize,
            self.algorithm.frames
        )
