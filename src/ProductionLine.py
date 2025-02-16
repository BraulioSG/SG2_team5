import simpy

from Resuppliers import Supplier, SuppliersContainer
from WorkStation import WorkStation

class ProductionLine(object):
    def __init__(self,id: int, env: simpy.Environment):
        self._env = env
        self._id = id;
        self._work_stations = list()
        self._suppliers = SuppliersContainer(env, 3)

        #Report Attributes
        self._production_times = list()


    def work(self) -> simpy.Process:
        start = self._env.now
        for ws in self._work_stations:
            yield self._env.process(ws.work())

        end = self._env.now
        delta_time = end - start 
        print("\n+-----+---------+---------+------+")
        print("| #ID |  START  | FINISH  |  DT  |")
        print("+-----+---------+---------+------+")
        print("| #%2d | %5.2f | %5.2f | %3.2f |" % (self._id, start, end, delta_time))
        print("+-----+---------+---------+------+")
        self._production_times.append(delta_time)

    def add_work_station(self, work_station: WorkStation) -> None:
        work_station.set_suppliers(self._suppliers)
        self._work_stations.append(work_station)

    def get_id(self) -> int:
        """ Returns the id of the production line """
        return self._id

    def get_max_time(self) -> int:
        """ Returns the maximum time of the production times """
        return max(self._production_times)

    def get_min_time(self) -> int:
        """ Returns the minimum time of the production times """
        return min(self._production_times)

    def get_avg_time(self) -> int:
        """ Returns the average time of the production times """
        return sum(self._production_times)/len(self._production_times)
