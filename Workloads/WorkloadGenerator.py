import random

class WorkloadGenerator:
    @staticmethod
    def sequential(start, length, numRepeats=1):
        workload = []
        for _ in range(numRepeats):
            workload.extend(range(start, start + length))
        return workload
    
    @staticmethod
    def random(pageRange, length, seed=None):
        if seed is not None:
            random.seed(seed)
        return [random.randint(0, pageRange - 1) for _ in range(length)]
    
    @staticmethod
    def localityBased(numLocalities, pagesPerLocality, accessesPerLocality, localityPageRange):
        workload = []
        
        for _ in range(numLocalities):
            localityStart = random.randint(0, localityPageRange - pagesPerLocality)
            localityPages = list(range(localityStart, localityStart + pagesPerLocality))
            
            for _ in range(accessesPerLocality):
                workload.append(random.choice(localityPages))
        
        return workload
    
    @staticmethod
    def looping(pattern, numLoops):
        return pattern * numLoops
    
    @staticmethod
    def mixed(sequentialRatio, randomRatio, localityRatio, totalLength, pageRange):
        workload = []
        
        sequentialLength = int(totalLength * sequentialRatio)
        randomLength = int(totalLength * randomRatio)
        localityLength = totalLength - sequentialLength - randomLength
        
        if sequentialLength > 0:
            workload.extend(WorkloadGenerator.sequential(0, sequentialLength))
        
        if randomLength > 0:
            workload.extend(WorkloadGenerator.random(pageRange, randomLength))
        
        if localityLength > 0:
            numLocalities = max(1, localityLength // 50)
            accessesPerLocality = localityLength // numLocalities
            workload.extend(WorkloadGenerator.localityBased(
                numLocalities, 10, accessesPerLocality, pageRange
            ))
        
        random.shuffle(workload)
        return workload
    
    @staticmethod
    def realistic(totalLength, pageRange, workingSetSize=20):
        workload = []
        currentWorkingSet = random.sample(range(pageRange), min(workingSetSize, pageRange))
        
        for i in range(totalLength):
            if random.random() < 0.8:
                workload.append(random.choice(currentWorkingSet))
            else:
                workload.append(random.randint(0, pageRange - 1))
            
            if i % 100 == 0 and random.random() < 0.3:
                numToReplace = random.randint(1, max(1, workingSetSize // 4))
                for _ in range(numToReplace):
                    if currentWorkingSet:
                        currentWorkingSet.pop(random.randint(0, len(currentWorkingSet) - 1))
                    newPage = random.randint(0, pageRange - 1)
                    if newPage not in currentWorkingSet:
                        currentWorkingSet.append(newPage)
        
        return workload