import matplotlib.pyplot as plt
import numpy as np

class PlotGenerator:
    def __init__(self, dataFrame):
        self.dataFrame = dataFrame
    
    def plotCumulativePageFaults(self):
        plt.figure(figsize=(10, 6))
        plt.plot(self.dataFrame["time"], self.dataFrame["pageFault"].cumsum())
        plt.xlabel("Time")
        plt.ylabel("Cumulative Page Faults")
        plt.title("Cumulative Page Faults vs Time")
        plt.grid(True, alpha=0.3)
        plt.show()
    
    def plotWorkingSetSize(self):
        plt.figure(figsize=(10, 6))
        plt.plot(self.dataFrame["time"], self.dataFrame["workingSetSize"])
        plt.xlabel("Time")
        plt.ylabel("Working Set Size")
        plt.title("Working Set Size vs Time")
        plt.grid(True, alpha=0.3)
        plt.show()
    
    def plotTlbHits(self):
        plt.figure(figsize=(10, 6))
        plt.plot(self.dataFrame["time"], self.dataFrame["tlbHit"].astype(int))
        plt.xlabel("Time")
        plt.ylabel("TLB Hit (1=Hit, 0=Miss)")
        plt.title("TLB Hit Behavior Over Time")
        plt.grid(True, alpha=0.3)
        plt.show()
    
    def plotPageFaultRate(self, windowSize=50):
        plt.figure(figsize=(10, 6))
        rollingFaults = self.dataFrame["pageFault"].rolling(window=windowSize).mean()
        plt.plot(self.dataFrame["time"], rollingFaults)
        plt.xlabel("Time")
        plt.ylabel(f"Page Fault Rate (over {windowSize} accesses)")
        plt.title("Page Fault Rate Over Time")
        plt.grid(True, alpha=0.3)
        plt.show()
    
    @staticmethod
    def compareAlgorithms(results):
        algorithms = list(results.keys())
        pageFaults = [results[alg]["totalPageFaults"] for alg in algorithms]
        
        plt.figure(figsize=(10, 6))
        bars = plt.bar(algorithms, pageFaults, color=['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4'])
        plt.xlabel("Algorithm")
        plt.ylabel("Total Page Faults")
        plt.title("Page Faults Comparison Across Algorithms")
        plt.grid(True, alpha=0.3, axis='y')
        
        for bar in bars:
            height = bar.get_height()
            plt.text(bar.get_x() + bar.get_width()/2., height,
                    f'{int(height)}',
                    ha='center', va='bottom')
        
        plt.show()
    
    @staticmethod
    def compareCumulativePageFaults(resultsDict):
        plt.figure(figsize=(12, 7))
        
        colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4', '#FFA07A', '#98D8C8']
        
        for idx, (algorithmName, dataFrame) in enumerate(resultsDict.items()):
            cumulativeFaults = dataFrame["pageFault"].cumsum()
            plt.plot(dataFrame["time"], cumulativeFaults, 
                    label=algorithmName, linewidth=2, color=colors[idx % len(colors)])
        
        plt.xlabel("Time")
        plt.ylabel("Cumulative Page Faults")
        plt.title("Cumulative Page Faults Comparison")
        plt.legend()
        plt.grid(True, alpha=0.3)
        plt.show()
    
    @staticmethod
    def compareMetrics(results):
        algorithms = list(results.keys())
        
        metrics = {
            "Page Fault Rate": [results[alg]["pageFaultRate"] for alg in algorithms],
            "TLB Hit Rate": [results[alg]["tlbHitRate"] for alg in algorithms]
        }
        
        x = np.arange(len(algorithms))
        width = 0.35
        
        fig, ax = plt.subplots(figsize=(12, 6))
        
        for idx, (metricName, values) in enumerate(metrics.items()):
            offset = width * (idx - 0.5)
            bars = ax.bar(x + offset, values, width, label=metricName)
            
            for bar in bars:
                height = bar.get_height()
                ax.text(bar.get_x() + bar.get_width()/2., height,
                       f'{height:.3f}',
                       ha='center', va='bottom', fontsize=9)
        
        ax.set_xlabel("Algorithm")
        ax.set_ylabel("Rate")
        ax.set_title("Performance Metrics Comparison")
        ax.set_xticks(x)
        ax.set_xticklabels(algorithms)
        ax.legend()
        ax.grid(True, alpha=0.3, axis='y')
        
        plt.tight_layout()
        plt.show()
    
    @staticmethod
    def heatmapFrameOccupancy(dataFrame, frameLimit):
        plt.figure(figsize=(14, 6))
        
        timeSteps = dataFrame["time"].values
        frameOccupancy = np.zeros((frameLimit, len(timeSteps)))
        
        for idx, frames in enumerate(dataFrame["frames"]):
            for frameIdx, page in enumerate(frames):
                if frameIdx < frameLimit:
                    frameOccupancy[frameIdx][idx] = page + 1
        
        plt.imshow(frameOccupancy, aspect='auto', cmap='viridis', interpolation='nearest')
        plt.colorbar(label='Page Number')
        plt.xlabel("Time")
        plt.ylabel("Frame Number")
        plt.title("Frame Occupancy Heatmap Over Time")
        plt.tight_layout()
        plt.show()
    
    @staticmethod
    def plotWorkloadPattern(workload):
        plt.figure(figsize=(12, 6))
        plt.plot(range(len(workload)), workload, linewidth=0.5, alpha=0.7)
        plt.xlabel("Access Index")
        plt.ylabel("Page Number")
        plt.title("Workload Access Pattern")
        plt.grid(True, alpha=0.3)
        plt.tight_layout()
        plt.show()