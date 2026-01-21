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

    parser.add_argument("--algo", required=True)
    parser.add_argument("--frames", type=int, required=True)
    parser.add_argument("--workload", required=True)
    parser.add_argument("--length", type=int, required=True)
    parser.add_argument("--tlb", type=int, default=0)

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

    metrics = MetricsComputer.compute(logger.records)
    MetricsComputer.save(metrics, "output/metrics.txt")

    PlotGenerator.generate(logger.records, outputDir="output")

    print("Simulation completed")
    print(f"Algorithm: {args.algo.upper()}")
    print(f"Frames: {args.frames}")
    print(f"Accesses: {args.length}")
    print(f"Page Faults: {metrics['totalPageFaults']}")
    print(f"Page Fault Rate: {metrics['pageFaultRate']:.3f}")

    if tlb is not None:
        print(f"TLB Hit Rate: {metrics['tlbHitRate']:.3f}")


if __name__ == "__main__":
    main()
