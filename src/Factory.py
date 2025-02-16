import simpy

from ProductionLine import ProductionLine;

class Factory(object):
    def __init__(self, open_time:int, env: simpy.Environment):
        self._env = env
        self._open_time = open_time;
        self._production_lines = list()
        self.action = self._env.process(self.work())

    def work(self) -> simpy.Process:
        print("Factory Opened")
        while True:
            try:
                for pl in self._production_lines:
                    yield self._env.process(pl.work())

            except simpy.Interrupt:
                print("Factory Closed")
                break

    def add_production_line(self, prodLine: ProductionLine) -> None:
        self._production_lines.append(prodLine)

    def get_production_lines(self) -> list:
        return self._production_lines;
