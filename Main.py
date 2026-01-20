from Algorithms.FIFO import FIFO
from Algorithms.LRU import LRU
from Algorithms.Optimal import Optimal

referenceString = [1, 2, 3, 4, 1, 2, 5]
frameLimit = 3

algorithm = LRU(frameLimit)

time = 0
for page in referenceString:
    algorithm.AccessPage(page, time)
    time += 1

print("Page Faults:", algorithm.GetPageFaults())
