class WorkingSetModel:
    def __init__(self, window_size):
        self.WindowSize = window_size
        self.AccessHistory = []

    def RecordAccess(self, page, time):
        self.AccessHistory.append((time, page))
        self.AccessHistory = [
            (t, p) for (t, p) in self.AccessHistory
            if time - t <= self.WindowSize
        ]

    def GetWorkingSet(self):
        return set(p for (_, p) in self.AccessHistory)

    def WorkingSetSize(self):
        return len(self.GetWorkingSet())

    def IsThrashing(self, frame_count):
        return self.WorkingSetSize() > frame_count
