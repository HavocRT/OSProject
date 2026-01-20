import pandas as pd

class MetricsAnalyzer:
    def __init__(self, records):
        self.dataFrame = pd.DataFrame(records)

    def totalPageFaults(self):
        return self.dataFrame["pageFault"].sum()

    def pageFaultRate(self):
        return self.dataFrame["pageFault"].mean()

    def tlbHitRate(self):
        return self.dataFrame["tlbHit"].mean()

    def averageWorkingSetSize(self):
        return self.dataFrame["workingSetSize"].mean()

    def cumulativePageFaults(self):
        return self.dataFrame["pageFault"].cumsum()

    def getDataFrame(self):
        return self.dataFrame
