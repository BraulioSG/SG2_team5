import simpy

from Resuppliers import SuppliersContainer


class Bin:
    def __init__(self):
        self.material_units = 25
        self.empty = False

    def use_material(self):
        if self.material_units > 0:
            self.material_units -= 1
            return True
        else:
            return False

    def resupply(self):
        self.material_units = 25
        self.empty = False

class WorkStation(object):
    def __init__(self, env: simpy.Environment, suppliers: SuppliersContainer) -> None:
        self._env = env
        self.bin = Bin()
        self.suppliers = suppliers

    def process(self) -> simpy.Process:
        while True:
            try:
                if self.bin.use_material():
                    #Process
                    print("Used material\n")
                else:
                    supplier = self.suppliers.check_for_available()
                    if supplier:
                        supplier.resupply(self)
            except simpy.Interrupt:
                print("Work Station finished work\n")
