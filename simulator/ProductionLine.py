import simpy

from WorkStation import WorkStation
from Item import Item

class ProductionLine(object):
    """ ProductionLine representation in a class 
    is in charge of controlling the manufacturing process and workstations
    """
    def __init__(self, prod_id: str, failure_probs: list, app, suppliers: simpy.Resource, env: simpy.Environment):
        self._env = env
        self._id = prod_id
        self._app = app
        self._work_stations = list()
        self._failure_probs = failure_probs
        self._suppliers = suppliers
        self._setup_production_line()
        self._action = None
        #Report Attributes
        self._production_times = list()
        self._ongoing_items = list()
        self._approved_items = 0
        self._rejected_items = 0

    def get_action(self):
        return self._action

    def _setup_production_line(self) -> None:
        #print(f"Setting up the PL#{self._id}...")
        for fail_prob in self._failure_probs:
            ws_id = f"WS#{len(self._work_stations)+1}@{self._id}"
            self._work_stations.append(WorkStation(ws_id, fail_prob, self._app, self._suppliers, self._env))
            #print(f"Work Station created with id: {ws_id}")

    def start(self):
        self._action = self._env.process(self.work())

    def work(self):
        try:
            while True:
                if self._work_stations[0].is_busy() == False:
                    self._ongoing_items.append(Item(self._env))

                for item in self._ongoing_items:
                    idx = item.get_current_stage()
                    if idx >= len(self._work_stations):
                        if item.is_approved():
                            self._approved_items += 1
                        else:
                            self._rejected_items += 1

                        self._production_times.append(item.get_production_time())
                        self._ongoing_items.remove(item)
                        continue

                    if self._work_stations[idx].is_busy() == False:
                        self._env.process(self._work_stations[idx].work(item))

                yield self._env.timeout(1)

            end = self._env.now
            delta_time = end - start 
            #print(f"[{self._id}] ended at {end} with a duration of {delta_time}")
            self._production_times.append(delta_time)
        except simpy.Interrupt:
            self.alarm()
            #print("PRODUCTION LINE STOPPED")
            return


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
        """ Returns the average time of the production times or 0 if the len is 0 """
        if len(self._production_times) == 0:
            return 0.0
        return sum(self._production_times)/len(self._production_times)

    def alarm(self):
        for ws in self._work_stations:
            ws_process = ws.get_process()
            if ws_process and ws_process.is_alive:
                ws_process.interrupt()
            ws.interrupt_ws()

    def print_report(self) -> None:
        total_items = self._approved_items + self._rejected_items
        fixing_times = list()
        supply_times = list()
        print(f"OVERVIEW ${self._id}")
        for ws in self._work_stations:
            ws.print_report()
            fixing_times.append(ws.get_avg_fixing_time())
            supply_times.append(ws.get_avg_supplying_time())

        if total_items > 0:
            print(f"\tApproved items: {self._approved_items} ({(self._approved_items/total_items)*100}%)")
            print(f"\tRejected items: {self._rejected_items} ({(self._rejected_items/total_items)*100}%)")
        print(f"\ttotal items: {self._approved_items + self._rejected_items}")

    def print_for_csv(self):
        total_items = self._approved_items + self._rejected_items
        for ws in self._work_stations:
            line = (f"{self._id}, {self._approved_items}, {self._rejected_items}, {total_items}, {ws.get_id()}, "
                    f"{ws.get_avg_fixing_time()}, {ws.get_avg_supplying_time()}, {ws.get_avg_production_time()}, {self.get_avg_time()}")
            print(line)
