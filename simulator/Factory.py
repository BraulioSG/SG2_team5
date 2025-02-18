import simpy

from ProductionLine import ProductionLine

class Factory(object):
    """ Class Representation for the Factory
    it handles all production lines and suppliers
    """
    def __init__(self, env: simpy.Environment, app, num_suppliers:int = 3) -> None:
        self._env = env
        self._production_lines = list()
        self._app = app
        self._suppliers = simpy.Resource(self._env, capacity=num_suppliers)
        self._action = None

    def start(self) -> None: 
        if len(self._production_lines) < 1:
            raise Exception("To start the factory you need at least one production line, use the method \"add_production_line\" to create a new Production Line")

        self._action = self._env.process(self.work())

    def work(self):
        #print("Factory Opened")
        for pl in self._production_lines:
            #self._env.process(pl.start())
            pl.start()

        while True:
            try:
                yield self._env.timeout(1)
            except simpy.Interrupt:
                self.alarm()
                return

    def get_action(self):
        return self._action

    def add_production_line(self, work_stations_failure_probs: list) -> None:
        """ Creates a new Production Line with workstations with the failures specified """
        prod_id = f"PL#{len(self._production_lines) + 1}"        

        production_line = ProductionLine(prod_id, work_stations_failure_probs, self._app, self._suppliers, self._env)
        self._production_lines.append(production_line)

    def get_production_lines(self) -> list:
        return self._production_lines

    def alarm(self):
        for pl in self._production_lines:
            action = pl.get_action()
            if action and action.is_alive:
                action.interrupt()

    def print_report(self) -> None:
        """ Displays the information to see the details of the simulation """
        for pl in self._production_lines:
            pl.print_report()

    def print_for_csv(self) -> None:
        """ Prints the results of the simulation in csv format """
        for pl in self._production_lines:
            pl.print_for_csv()
