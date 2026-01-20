class MemoryLogger:
    def __init__(self):
        self.records = []

    def logStep(self, time, page, pageFault, tlbHit, workingSetSize, frames):
        self.records.append({
            "time": time,
            "page": page,
            "pageFault": pageFault,
            "tlbHit": tlbHit,
            "workingSetSize": workingSetSize,
            "frames": list(frames)
        })

    def getRecords(self):
        return self.records
