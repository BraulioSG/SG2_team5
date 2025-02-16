from WorkStation import WorkStation
import simpy
import random as rd


class SuppliersContainer:
    def __init__(self, env: simpy.Environment, amount):
        self.suppliers = list()
        for i in range(amount):
            self.suppliers.append(Supplier(env))

    def check_for_available(self):
        for supplier in self.suppliers:
            if not supplier.busy:
                return supplier

        return False


class Supplier:
    def __init__(self, _env: simpy.Environment):
        self.busy = False
        self.env = _env

    def resupply(self, station: WorkStation) -> simpy.Process:
        if self.busy:
            return

        supply_time = 2

        self.busy = True
        station.bin.resupply()
        yield self.env.timeout(rd.normalvariate(supply_time))
