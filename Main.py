from Algorithms.IPRA import IPRA
from Algorithms.TLB import TLB
from Simulator.MemorySimulator import MemorySimulator

ipra = IPRA(frames=3, window_size=4)
tlb = TLB(size=2)

sim = MemorySimulator(ipra, tlb)

reference_string = [1, 2, 3, 1, 4, 1, 2, 5]

for page in reference_string:
    sim.AccessPage(page)

print("Page Faults:", ipra.PageFaults)
print("TLB Hit Rate:", tlb.HitRate())
