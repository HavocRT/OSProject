import argparse

from Simulator.MemorySimulator import MemorySimulator
from Logger.MemoryLogger import MemoryLogger
from Workloads.WorkloadGenerator import WorkloadGenerator
from Analysis.MetricsAnalyzer import MetricsAnalyzer
from Analysis.PlotGenerator import PlotGenerator

from Algorithms.FIFO import FIFO
from Algorithms.LRU import LRU
from Algorithms.Optimal import Optimal
from Algorithms.IPRA import IPRA
from Algorithms.TLB import TLB


def buildAlgorithm(algoName, frameLimit, referenceString):
    algoName = algoName.lower()

    if algoName == "fifo":
        return FIFO(frameLimit)

    if algoName == "lru":
        return LRU(frameLimit)

    if algoName == "optimal":
        return Optimal(frameLimit, referenceString)

    if algoName == "ipra":
        return IPRA(frameLimit, windowSize=10)

    raise ValueError("Unknown algorithm")


def runSingleAlgorithm(algoName, frameLimit, referenceString, tlbSize):
    algorithm = buildAlgorithm(algoName, frameLimit, referenceString)
    tlb = TLB(tlbSize) if tlbSize > 0 else None
    logger = MemoryLogger()

    simulator = MemorySimulator(
        algorithm=algorithm,
        tlb=tlb,
        logger=logger
    )

    simulator.run(referenceString)
    
    return logger.getRecords(), algorithm


def main():
    parser = argparse.ArgumentParser()
    
    parser.add_argument("--algo", required=True) #Algorithm: fifo, lru, optimal, ipra, OR comma-separated list like "fifo,lru,ipra"
    parser.add_argument("--frames", type=int, required=True) #Number of frames
    parser.add_argument("--workload", required=True) #Workload type: locality, thrashing, mixed
    parser.add_argument("--length", type=int, required=True) #Length of reference string
    parser.add_argument("--tlb", type=int, default=0) #TLB size (0 for no TLB)

    args = parser.parse_args()

    algorithms = [algo.strip() for algo in args.algo.split(",")]

    referenceString = WorkloadGenerator.generate(
        workloadType=args.workload,
        length=args.length
    )

    results = {}
    
    print("\n" + "="*50)
    print("Running Simulations")
    print("="*50)

    for algoName in algorithms:
        print(f"Running {algoName.upper()}...")
        records, algorithm = runSingleAlgorithm(
            algoName=algoName,
            frameLimit=args.frames,
            referenceString=referenceString,
            tlbSize=args.tlb
        )
        
        analyzer = MetricsAnalyzer(records)
        
        results[algoName] = {
            "records": records,
            "analyzer": analyzer,
            "algorithm": algorithm
        }

    print("\n" + "="*50)
    print("Comparison Results")
    print("="*50)
    print(f"Workload: {args.workload}")
    print(f"Frames: {args.frames}")
    print(f"Reference String Length: {args.length}")
    print("-"*50)

    for algoName in algorithms:
        analyzer = results[algoName]["analyzer"]
        totalPageFaults = analyzer.totalPageFaults()
        pageFaultRate = analyzer.pageFaultRate()
        
        print(f"\n{algoName.upper()}:")
        print(f"  Total Page Faults: {totalPageFaults}")
        print(f"  Page Fault Rate: {pageFaultRate:.3f}")
        
        if args.tlb > 0:
            tlbHitRate = analyzer.tlbHitRate()
            print(f"  TLB Hit Rate: {tlbHitRate:.3f}")
        
        if algoName.lower() == "ipra":
            avgWorkingSetSize = analyzer.averageWorkingSetSize()
            print(f"  Average Working Set Size: {avgWorkingSetSize:.2f}")

    print("\n" + "="*50 + "\n")

    if len(algorithms) > 1:
        print("Generating comparison plots...")
        import matplotlib.pyplot as plt
        
        plt.figure(figsize=(10, 6))
        for algoName in algorithms:
            analyzer = results[algoName]["analyzer"]
            df = analyzer.getDataFrame()
            plt.plot(df["time"], df["pageFault"].cumsum(), label=algoName.upper(), linewidth=2)
        
        plt.xlabel("Time")
        plt.ylabel("Cumulative Page Faults")
        plt.title("Algorithm Comparison: Cumulative Page Faults")
        plt.legend()
        plt.grid(True, alpha=0.3)
        plt.tight_layout()
        plt.show()
        
        if args.tlb > 0:
            plt.figure(figsize=(10, 6))
            for algoName in algorithms:
                analyzer = results[algoName]["analyzer"]
                df = analyzer.getDataFrame()
                plt.plot(df["time"], df["tlbHit"].astype(int), label=algoName.upper(), alpha=0.7)
            
            plt.xlabel("Time")
            plt.ylabel("TLB Hit (1=Hit, 0=Miss)")
            plt.title("Algorithm Comparison: TLB Hit Behavior")
            plt.legend()
            plt.grid(True, alpha=0.3)
            plt.tight_layout()
            plt.show()
        
        if "ipra" in [algo.lower() for algo in algorithms]:
            plt.figure(figsize=(10, 6))
            analyzer = results["ipra"]["analyzer"]
            df = analyzer.getDataFrame()
            plt.plot(df["time"], df["workingSetSize"], color='purple', linewidth=2)
            plt.axhline(y=args.frames, color='r', linestyle='--', label=f'Frame Limit ({args.frames})')
            plt.xlabel("Time")
            plt.ylabel("Working Set Size")
            plt.title("IPRA: Working Set Size Over Time")
            plt.legend()
            plt.grid(True, alpha=0.3)
            plt.tight_layout()
            plt.show()
    
    else:
        print("Generating plots...")
        algoName = algorithms[0]
        analyzer = results[algoName]["analyzer"]
        plotter = PlotGenerator(analyzer.getDataFrame())
        
        plotter.plotCumulativePageFaults()
        
        if args.tlb > 0:
            plotter.plotTlbHits()
        
        if algoName.lower() == "ipra":
            plotter.plotWorkingSetSize()

    print("Simulation completed!")


if __name__ == "__main__":
    main()