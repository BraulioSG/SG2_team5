import simpy

from ProductionLine import ProductionLine;

class Factory(object):
    def __init__(self, env: simpy.Environment):
        self._env = env
        self.production_lines = list()

    def process(self) -> simpy.Process:
        yield self._env.timeout(1)

    def add_production_line(self, prodLine: ProductionLine) -> None:
        self.production_lines.append(prodLine)
