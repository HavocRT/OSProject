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


def main():
    parser = argparse.ArgumentParser()

    parser.add_argument("--algo", required=True, help="Algorithm: fifo, lru, optimal, ipra")
    parser.add_argument("--frames", type=int, required=True, help="Number of frames")
    parser.add_argument("--workload", required=True, help="Workload type: locality, thrashing, mixed")
    parser.add_argument("--length", type=int, required=True, help="Length of reference string")
    parser.add_argument("--tlb", type=int, default=0, help="TLB size (0 for no TLB)")

    args = parser.parse_args()

    referenceString = WorkloadGenerator.generate(
        workloadType=args.workload,
        length=args.length
    )

    algorithm = buildAlgorithm(
        algoName=args.algo,
        frameLimit=args.frames,
        referenceString=referenceString
    )

    tlb = TLB(args.tlb) if args.tlb > 0 else None
    logger = MemoryLogger()

    simulator = MemorySimulator(
        algorithm=algorithm,
        tlb=tlb,
        logger=logger
    )

    simulator.run(referenceString)

    analyzer = MetricsAnalyzer(logger.getRecords())
    
    totalPageFaults = analyzer.totalPageFaults()
    pageFaultRate = analyzer.pageFaultRate()
    
    # Print results
    print("\n" + "="*50)
    print("Simulation Results")
    print("="*50)
    print(f"Algorithm: {args.algo.upper()}")
    print(f"Frames: {args.frames}")
    print(f"Reference String Length: {args.length}")
    print(f"Total Page Faults: {totalPageFaults}")
    print(f"Page Fault Rate: {pageFaultRate:.3f}")

    if tlb is not None:
        tlbHitRate = analyzer.tlbHitRate()
        print(f"TLB Hit Rate: {tlbHitRate:.3f}")

    if args.algo.lower() == "ipra":
        avgWorkingSetSize = analyzer.averageWorkingSetSize()
        print(f"Average Working Set Size: {avgWorkingSetSize:.2f}")

    print("="*50 + "\n")

    # Generate plots
    print("Generating plots...")
    plotter = PlotGenerator(analyzer.getDataFrame())
    
    plotter.plotCumulativePageFaults()
    
    if tlb is not None:
        plotter.plotTlbHits()
    
    if args.algo.lower() == "ipra":
        plotter.plotWorkingSetSize()

    print("Simulation completed!")


if __name__ == "__main__":
    main()