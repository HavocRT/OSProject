import argparse
from Algorithms.FIFO import FIFO
from Algorithms.LRU import LRU
from Algorithms.Optimal import Optimal
from Algorithms.IPRA import IPRA
from Algorithms.TLB import TLB
from Workloads.WorkloadGenerator import WorkloadGenerator
from Simulator.MemorySimulator import MemorySimulator
from Logger.MemoryLogger import MemoryLogger
from Analysis.MetricsAnalyzer import MetricsAnalyzer
from Analysis.PlotGenerator import PlotGenerator

def parseArguments():
    parser = argparse.ArgumentParser()
    
    parser.add_argument('--algorithms', nargs='+', 
                       choices=['FIFO', 'LRU', 'Optimal', 'IPRA', 'All'],
                       default=['All'])
    
    parser.add_argument('--frames', type=int, default=4)
    
    parser.add_argument('--workload', 
                       choices=['sequential', 'random', 'locality', 'looping', 'mixed', 'realistic'],
                       default='realistic')
    
    parser.add_argument('--tlb-size', type=int, default=None)
    
    parser.add_argument('--tau', type=int, default=20)
    
    return parser.parse_args()

def generateWorkload(workloadType):
    length = 1000
    pageRange = 20
    
    if workloadType == 'sequential':
        return WorkloadGenerator.sequential(0, length)
    elif workloadType == 'random':
        return WorkloadGenerator.random(pageRange, length)
    elif workloadType == 'locality':
        numLocalities = 10
        accessesPerLocality = 100
        return WorkloadGenerator.localityBased(numLocalities, 10, accessesPerLocality, pageRange)
    elif workloadType == 'looping':
        pattern = list(range(10))
        numLoops = 100
        return WorkloadGenerator.looping(pattern, numLoops)
    elif workloadType == 'mixed':
        return WorkloadGenerator.mixed(0.3, 0.3, 0.4, length, pageRange)
    elif workloadType == 'realistic':
        return WorkloadGenerator.realistic(length, pageRange)
    
    return []

def createAlgorithm(algorithmName, frameLimit, referenceString, tau):
    if algorithmName == 'FIFO':
        return FIFO(frameLimit)
    elif algorithmName == 'LRU':
        return LRU(frameLimit)
    elif algorithmName == 'Optimal':
        return Optimal(frameLimit, referenceString)
    elif algorithmName == 'IPRA':
        return IPRA(frameLimit, tau)
    
    return None

def runSimulation(algorithmName, algorithm, referenceString, tlbSize):
    logger = MemoryLogger()
    tlb = TLB(tlbSize, "LRU") if tlbSize is not None else None
    
    simulator = MemorySimulator(algorithm, tlb, logger)
    simulator.run(referenceString)
    
    records = logger.getRecords()
    analyzer = MetricsAnalyzer(records)
    
    results = {
        'algorithmName': algorithmName,
        'totalPageFaults': analyzer.totalPageFaults(),
        'pageFaultRate': analyzer.pageFaultRate(),
        'tlbHitRate': analyzer.tlbHitRate() if tlbSize is not None else 0.0,
        'averageWorkingSetSize': analyzer.averageWorkingSetSize(),
        'dataFrame': analyzer.getDataFrame()
    }
    
    return results

def main():
    args = parseArguments()
    
    print("=" * 60)
    print("Page Replacement Algorithm Simulator")
    print("=" * 60)
    
    referenceString = generateWorkload(args.workload)
    
    print(f"\nWorkload: {args.workload}")
    print(f"Frames: {args.frames}")
    print(f"TLB: {'Enabled (size=' + str(args.tlb_size) + ')' if args.tlb_size else 'Disabled'}")
    print(f"Tau (Working Set Window): {args.tau}")
    
    algorithmsToRun = args.algorithms
    if 'All' in algorithmsToRun:
        algorithmsToRun = ['FIFO', 'LRU', 'Optimal', 'IPRA']
    
    print(f"Algorithms: {', '.join(algorithmsToRun)}")
    print("=" * 60)
    
    allResults = {}
    dataFrames = {}
    
    for algorithmName in algorithmsToRun:
        print(f"\nRunning {algorithmName}...")
        
        algorithm = createAlgorithm(algorithmName, args.frames, referenceString, args.tau)
        
        if algorithm is None:
            print(f"Error: Unable to create {algorithmName} algorithm")
            continue
        
        results = runSimulation(algorithmName, algorithm, referenceString, args.tlb_size)
        
        allResults[algorithmName] = results
        dataFrames[algorithmName] = results['dataFrame']
        
        print(f"  Page Faults: {results['totalPageFaults']}")
        print(f"  Fault Rate: {results['pageFaultRate']:.4f}")
        if args.tlb_size is not None:
            print(f"  TLB Hit Rate: {results['tlbHitRate']:.4f}")
    
    print("\n" + "=" * 60)
    print("Results")
    print("=" * 60)
    
    if len(allResults) > 1:
        PlotGenerator.compareAlgorithms(allResults)
        PlotGenerator.compareCumulativePageFaults(dataFrames)
        if args.tlb_size is not None:
            PlotGenerator.compareMetrics(allResults)

if __name__ == "__main__":
    main()