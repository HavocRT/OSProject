.PHONY: all clean help sequential random locality looping mixed realistic all-workloads \
        compare-frames compare-tlb compare-tau fifo-only lru-only optimal-only ipra-only \
        no-tlb with-tlb demo

PYTHON = python3
MAIN = Main.py

all:
	$(PYTHON) $(MAIN) --algorithms All --frames 4 --workload realistic --tlb-size 8 --tau 20

sequential:
	$(PYTHON) $(MAIN) --algorithms All --frames 4 --workload sequential --tlb-size 8 --tau 20

random:
	$(PYTHON) $(MAIN) --algorithms All --frames 4 --workload random --tlb-size 8 --tau 20

locality:
	$(PYTHON) $(MAIN) --algorithms All --frames 4 --workload locality --tlb-size 8 --tau 20

looping:
	$(PYTHON) $(MAIN) --algorithms All --frames 4 --workload looping --tlb-size 8 --tau 20

mixed:
	$(PYTHON) $(MAIN) --algorithms All --frames 4 --workload mixed --tlb-size 8 --tau 20

realistic:
	$(PYTHON) $(MAIN) --algorithms All --frames 4 --workload realistic --tlb-size 8 --tau 20

all-workloads:
	@make sequential
	@make random
	@make locality
	@make looping
	@make mixed
	@make realistic

fifo-only:
	$(PYTHON) $(MAIN) --algorithms FIFO --frames 4 --workload realistic --tlb-size 8 --tau 20

lru-only:
	$(PYTHON) $(MAIN) --algorithms LRU --frames 4 --workload realistic --tlb-size 8 --tau 20

optimal-only:
	$(PYTHON) $(MAIN) --algorithms Optimal --frames 4 --workload realistic --tlb-size 8 --tau 20

ipra-only:
	$(PYTHON) $(MAIN) --algorithms IPRA --frames 4 --workload realistic --tlb-size 8 --tau 20

compare-frames:
	$(PYTHON) $(MAIN) --algorithms All --frames 2 --workload realistic --tlb-size 8 --tau 20
	$(PYTHON) $(MAIN) --algorithms All --frames 4 --workload realistic --tlb-size 8 --tau 20
	$(PYTHON) $(MAIN) --algorithms All --frames 8 --workload realistic --tlb-size 8 --tau 20
	$(PYTHON) $(MAIN) --algorithms All --frames 16 --workload realistic --tlb-size 8 --tau 20

compare-tlb:
	$(PYTHON) $(MAIN) --algorithms All --frames 4 --workload realistic --tlb-size 4 --tau 20
	$(PYTHON) $(MAIN) --algorithms All --frames 4 --workload realistic --tlb-size 8 --tau 20
	$(PYTHON) $(MAIN) --algorithms All --frames 4 --workload realistic --tlb-size 16 --tau 20
	$(PYTHON) $(MAIN) --algorithms All --frames 4 --workload realistic --tlb-size 32 --tau 20

compare-tau:
	$(PYTHON) $(MAIN) --algorithms IPRA --frames 4 --workload realistic --tlb-size 8 --tau 10
	$(PYTHON) $(MAIN) --algorithms IPRA --frames 4 --workload realistic --tlb-size 8 --tau 20
	$(PYTHON) $(MAIN) --algorithms IPRA --frames 4 --workload realistic --tlb-size 8 --tau 50
	$(PYTHON) $(MAIN) --algorithms IPRA --frames 4 --workload realistic --tlb-size 8 --tau 100

no-tlb:
	$(PYTHON) $(MAIN) --algorithms All --frames 4 --workload realistic --tau 20

with-tlb:
	$(PYTHON) $(MAIN) --algorithms All --frames 4 --workload realistic --tlb-size 8 --tau 20

demo:
	@make all
	@make ipra-only
	$(PYTHON) $(MAIN) --algorithms All --frames 4 --workload locality --tlb-size 8 --tau 20
	$(PYTHON) $(MAIN) --algorithms All --frames 4 --workload random --tlb-size 8 --tau 20

clean:
	rm -rf __pycache__
	rm -rf */__pycache__
	rm -rf */*/__pycache__
	rm -f *.pyc */*.pyc */*/*.pyc