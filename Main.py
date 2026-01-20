from Algorithms.IPRA import IPRA
from Algorithms.TLB import TLB
from Simulator.MemorySimulator import MemorySimulator

ipra = IPRA(frames=3, window_size=4)
tlb = TLB(size=2)

sim = MemorySimulator(ipra, tlb)

referenceString = [1, 2, 3, 1, 4, 1, 2, 5]

for page in referenceString:
    sim.accessPage(page)

print("Page Faults:", ipra.pageFaults)
print("TLB Hit Rate:", tlb.hitRate())
