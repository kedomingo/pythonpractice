class Schedule:

    def __init__(self, start, end):
        self.start = start
        self.end = end

    def get_start(self):
        return self.start

    def get_end(self):
        return self.end

    def to_string(self):
        return str(self.start) + ' - ' + str(self.end)

    # Get intersection with another schedule
    def get_intersection(self, schedule):
        start = max(self.get_start(), schedule.get_start())
        end = min(self.get_end(), schedule.get_end())
        return Schedule(start, end) if start <= end else None

    def intersect(self, schedules):
        intersection = self
        for sched in schedules:
            intersection = intersection.get_intersection(sched)
            if not intersection:
                return None
        return intersection


new_schedule = Schedule(8, 12)
schedules = [
    Schedule(10, 13),
    Schedule(9, 14),
]
expected = Schedule(10, 12)
actual = new_schedule.intersect(schedules)
# actual = 10-12
print(actual.to_string())

# actual = None
new_schedule = Schedule(16, 18)
actual = new_schedule.intersect(schedules)
print(actual)


