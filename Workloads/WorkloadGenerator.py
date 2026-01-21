import random

class WorkloadGenerator:
    def highLocality(self, pages, repetitions):
        workload = []
        for _ in range(repetitions):
            workload.extend(pages)
        return workload

    def phaseChange(self, phases, repetitionsPerPhase):
        workload = []
        for phase in phases:
            for _ in range(repetitionsPerPhase):
                workload.extend(phase)
        return workload

    def thrashing(self, uniquePages, length):
        return [random.randint(1, uniquePages) for _ in range(length)]

    def mixed(self, hotPages, coldPages, length, hotProbability=0.8):
        workload = []
        for _ in range(length):
            if random.random() < hotProbability:
                workload.append(random.choice(hotPages))
            else:
                workload.append(random.choice(coldPages))
        return workload

    @staticmethod
    def generate(workloadType, length):
        if workloadType == "locality":
            pages = [1, 2, 3]
            repetitions = length // len(pages)
            workload = []
            for _ in range(repetitions):
                workload.extend(pages)
            return workload[:length]

        if workloadType == "thrashing":
            return [random.randint(1, length) for _ in range(length)]

        if workloadType == "mixed":
            hotPages = [1, 2, 3]
            coldPages = list(range(4, 20))
            workload = []
            for _ in range(length):
                if random.random() < 0.8:
                    workload.append(random.choice(hotPages))
                else:
                    workload.append(random.choice(coldPages))
            return workload

        raise ValueError("Unknown workload type")
