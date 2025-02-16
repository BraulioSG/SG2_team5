import simpy

from Resuppliers import Supplier, SuppliersContainer
from WorkStation import WorkStation

class ProductionLine(object):
    def __init__(self,id: int, env: simpy.Environment):
        self._env = env
        self._id = id;
        self.work_stations = list()
        self.suppliers = SuppliersContainer(env, 3)

    def work(self) -> simpy.Process:
        for ws in self.work_stations:
            yield self._env.process(ws.work());

    def add_work_station(self, work_station: WorkStation) -> None:
        self.work_stations.append(work_station)

