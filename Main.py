import argparse
from Algorithms.IPRA import IPRA
from Algorithms.FIFO import FIFO
from Algorithms.LRU import LRU
from Algorithms.TLB import TLB
from Simulator.MemorySimulator import MemorySimulator
from Logger.MemoryLogger import MemoryLogger
from Workloads.WorkloadGenerator import WorkloadGenerator
from Analysis.MetricsAnalyzer import MetricsAnalyzer

def parseArguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("--algo", required=True, choices=["fifo", "lru", "ipra"])
    parser.add_argument("--processes", type=int, required=True)
    parser.add_argument("--frames", type=int, required=True)
    return parser.parse_args()

def createAlgorithm(algoName, frameLimit):
    if algoName == "fifo":
        return FIFO(frameLimit)
    if algoName == "lru":
        return LRU(frameLimit)
    if algoName == "ipra":
        return IPRA(frameLimit, windowSize=4)

def generateProcessWorkloads(processCount):
    generator = WorkloadGenerator()
    workloads = []

    for i in range(processCount):
        workload = generator.phaseChange(
            phases=[[1, 2, 3], [4, 5, 6]],
            repetitionsPerPhase=10
        )
        workloads.append(workload)

    return workloads

def interleaveWorkloads(workloads):
    interleaved = []
    maxLength = max(len(w) for w in workloads)

    for i in range(maxLength):
        for workload in workloads:
            if i < len(workload):
                interleaved.append(workload[i])

    return interleaved

def main():
    args = parseArguments()

    algorithm = createAlgorithm(args.algo, args.frames)
    tlb = TLB(size=4)
    logger = MemoryLogger()
    simulator = MemorySimulator(algorithm, tlb, logger)

    workloads = generateProcessWorkloads(args.processes)
    referenceString = interleaveWorkloads(workloads)

    for page in referenceString:
        simulator.accessPage(page)

    analyzer = MetricsAnalyzer(logger.getRecords())

    print("Algorithm:", args.algo)
    print("Processes:", args.processes)
    print("Frames:", args.frames)
    print("Total Page Faults:", analyzer.totalPageFaults())
    print("Page Fault Rate:", analyzer.pageFaultRate())
    print("TLB Hit Rate:", analyzer.tlbHitRate())
    print("Average Working Set Size:", analyzer.averageWorkingSetSize())

if __name__ == "__main__":
    main()
