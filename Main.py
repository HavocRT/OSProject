from Algorithms.IPRA import IPRA
from Algorithms.TLB import TLB
from Simulator.MemorySimulator import MemorySimulator
from Logger.MemoryLogger import MemoryLogger

ipra = IPRA(frames=3, windowSize=4)
tlb = TLB(size=2)
logger = MemoryLogger()

simulator = MemorySimulator(ipra, tlb, logger)

referenceString = [1, 2, 3, 1, 4, 1, 2, 5]

for page in referenceString:
    simulator.accessPage(page)

records = logger.getRecords()

for record in records:
    print(record)
