import matplotlib.pyplot as plt

class PlotGenerator:
    def __init__(self, dataFrame):
        self.dataFrame = dataFrame

    def plotCumulativePageFaults(self):
        plt.figure()
        plt.plot(self.dataFrame["time"], self.dataFrame["pageFault"].cumsum())
        plt.xlabel("Time")
        plt.ylabel("Cumulative Page Faults")
        plt.title("Cumulative Page Faults vs Time")
        plt.show()

    def plotWorkingSetSize(self):
        plt.figure()
        plt.plot(self.dataFrame["time"], self.dataFrame["workingSetSize"])
        plt.xlabel("Time")
        plt.ylabel("Working Set Size")
        plt.title("Working Set Size vs Time")
        plt.show()

    def plotTlbHits(self):
        plt.figure()
        plt.plot(self.dataFrame["time"], self.dataFrame["tlbHit"].astype(int))
        plt.xlabel("Time")
        plt.ylabel("TLB Hit (1=Hit, 0=Miss)")
        plt.title("TLB Hit Behavior Over Time")
        plt.show()
