import simpy

class Bin:
    def __init__(self):
        self.material_units = 25
        self.empty = False

    def use_material(self):
        self.material_units -= 1
        self.empty = True if self.material_units <= 0 else False

    def resupply(self):
        self.material_units = 25
        self.empty = False

class WorkStation(object):
    def __init__(self, _bin: Bin ,env: simpy.Environment) -> None:
        self._evn = env
        self.bin = _bin

    def process(self) -> simpy.Process:
        yield self._env.timeout(1)

