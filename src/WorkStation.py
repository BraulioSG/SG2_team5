import random
import simpy

from Bin import Bin
from Item import Item
from Utils import ColorsCLI

class WorkStation(object):
    def __init__(self, ws_id: str, failure_prob: float, suppliers: simpy.Resource, env: simpy.Environment) -> None:
        self._env = env
        self._bin = Bin()
        self._id = ws_id
        self._failure_probability = failure_prob
        self._suppliers = suppliers

        self._items_to_verification = 5
        self._failures = 0
        self._successes = 0
        self._busy = False
        
        #Report Attributes
        self._fixing_times = list()
        self._supplying_times = list()

    def get_id(self):
        return self._id

    def is_busy(self) -> bool:
        return self._busy

    def get_avg_fixing_time(self) -> int:
        if len(self._fixing_times) == 0:
            return 0.0

        return sum(self._fixing_times) / len(self._fixing_times)

    def get_avg_supplying_time(self) -> int:
        if len(self._supplying_times) == 0:
            return 0.0

        return sum(self._supplying_times) / len(self._supplying_times)

    def work(self, item: Item) -> simpy.Process:
        try:
            self._busy = True
            # Check if there is an incident
            if random.randint(0,100) < 1:
                #print(f"[{ColorsCLI.ERROR}INTERRUPTION{ColorsCLI.DEFAULT}] Critical error in the facility")
                return simpy.Interrupt('There was an accident in the facility that stopped production!')

            if(self._bin.is_empty()):
                yield self._env.process(self.look_for_supply())

            if self._items_to_verification <= 0:
                failure_chance = random.normalvariate(self._failure_probability)
                failure_chance = max(0, min(1, failure_chance))
                if random.random() < failure_chance:
                    #print(f"{self._id} test [{ColorsCLI.ERROR}FAILED{ColorsCLI.DEFAULT}]")
                    yield self._env.process(self.fix_work_station())
                else:
                    pass
                    #print(f"{self._id} test [{ColorsCLI.SUCCESS}SUCCESS{ColorsCLI.DEFAULT}]")
                self._items_to_verification = 5

            self._bin.use_material()
            self._items_to_verification -= 1
                
            yield self._env.timeout(random.normalvariate(4))

            item.update_end_time()
            item.next_stage()
            self._busy = False
        except simpy.Interrupt:
            return

    def fix_work_station(self) -> simpy.Process:
       # print(f"{self._id} status [{ColorsCLI.WARNING}FIXING - WORKSTATION{ColorsCLI.DEFAULT}]")

        start = self._env.now
        yield self._env.timeout(random.expovariate(3)) #fixing time
        end = self._env.now
        self._fixing_times.append(end - start)

    def look_for_supply(self) -> simpy.Process:
        #print(f"{self._id} status [{ColorsCLI.WARNING}SUPPLYING - WORKSTATION{ColorsCLI.DEFAULT}]")
        request = self._suppliers.request()

        start = self._env.now
        yield request #wait for supplier free
        self._bin.refill()
        self._suppliers.release(request)
        end = self._env.now

        self._supplying_times.append(end- start)

    def print_report(self) -> None:
        print(f"\tOVERVIEW ${self._id}")
        total_tests = self._failures + self._successes;
        if total_tests > 0:
            print(f"\ttests: {self._successes}/{total_tests} ({(self._successes/total_tests)*100}%)")
        print(f"\tavg fixing time: {self.get_avg_fixing_time()}")
        print(f"\tavg supply time: {self.get_avg_supplying_time()}")
