import simpy

from ProductionLine import ProductionLine

class Factory(object):
    """ Class Representation for the Factory
    Attributes:

    Methods:
    """
    def __init__(self, env: simpy.Environment, num_suppliers:int = 3) -> None:
        self._env = env
        self._production_lines = list()
        self._suppliers = simpy.Resource(self._env, capacity=num_suppliers)

    def start(self) -> None: 
        if len(self._production_lines) < 1:
            raise Exception("To start the factory you need at least one production line, use the method \"add_production_line\" to create a new Production Line")

        self.action = self._env.process(self.work())

    def work(self) -> simpy.Process:
        #print("Factory Opened")
        for pl in self._production_lines:
            self._env.process(pl.start())

        while True:
            try:
                yield self._env.timeout(1)
            except simpy.Interrupt:
                return simpy.Interrupt()

    def add_production_line(self, work_stations_failure_probs: list) -> None:
        """ Creates a new Production Line with workstations with the failures specified """
        prod_id = f"PL#{len(self._production_lines) + 1}"        

        production_line = ProductionLine(prod_id, work_stations_failure_probs, self._suppliers, self._env)
        self._production_lines.append(production_line)

    def get_production_lines(self) -> list:
        return self._production_lines

    def print_report(self) -> None:
        for pl in self._production_lines:
            pl.print_report()

    def print_for_csv(self) -> None:
        for pl in self._production_lines:
            pl.print_for_csv()
