class MemorySimulator:
    def __init__(self, algorithm, tlb=None, logger=None):
        self.algorithm = algorithm
        self.tlb = tlb
        self.logger = logger
        self.time = 0

    def accessPage(self, page):
        faultsBefore = self.algorithm.pageFaults

        if self.tlb is not None:
            tlbHit = self.tlb.accessPage(page, self.time)
        else:
            tlbHit = None

        self.algorithm.accessPage(page, self.time)

        faultOccurred = self.algorithm.pageFaults > faultsBefore

        if self.logger is not None:
            self.logger.log(
                time=self.time,
                page=page,
                pageFault=faultOccurred,
                tlbHit=tlbHit,
                frames=list(self.algorithm.frames)
            )

        self.time += 1

    def run(self, referenceString):
        for page in referenceString:
            self.accessPage(page)
