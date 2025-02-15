import simpy

from WorkStation import WorkStation;

class ProductionLine(object):
    def __init__(self, env: simpy.Environment):
        self._env = env
        self.work_stations = list();

    def process(self) -> simpy.Process:
        yield self._evn.timeout(1)

    def add_work_station(self, workStation: WorkStation) -> None:
        self.work_stations.append(workStation);

