from WorkStation import WorkStation
import simpy
import random as rd


class SuppliersContainer:
    def __init__(self, env: simpy.Environment, amount):
        self.suppliers = list()
        for i in range(amount - 1):
            self.suppliers.append(Supplier(env))


class Supplier:
    def __init__(self, _env: simpy.Environment):
        self.busy = False
        self.env = _env

    def resupply(self, station: WorkStation) -> simpy.Process:
        if not self.busy:
            self.busy = True
            station.bin.resupply()
            yield self.env.timeout(rd.normalvariate(2))