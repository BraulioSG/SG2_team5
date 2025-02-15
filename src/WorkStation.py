import simpy

from Resuppliers import SuppliersContainer


class Bin:
    def __init__(self, capacity: int = 25):
        self._material_units = capacity
        self._capacity = capacity
        self.empty = False

     def use_material(self):
        """ Decrease by one the material units, if is empty it will rise an exception """
        if(self.is_empty()):
            #raise Exception("Try to use material when the bin is empty")
            print("bin is empty")
            return

        self._material_units -= 1

    def resupply(self) -> None:
        """ Sets the material units to the same value as the capacity """
        self._material_units = self.capacity

    def get_remaining_units(self) -> int:
        """ Returns the number of material units remaining in the bin """
        return self._material_units

    def is_empty(self) -> bool:
        """ Returns true if the material units is less or equal to zero"""
        return self.get_remaining_units() <= 0

class WorkStation(object):
    def __init__(self, env: simpy.Environment, suppliers: SuppliersContainer) -> None:
        self._env = env
        self.bin = Bin()
        self.suppliers = suppliers

    def work(self) -> simpy.Process:
        print(f"WS#{self._id}\tstarted \tt={self._env.now}")
        if(self._bin.is_empty()):
            #Do the resuply process
            print(f"WS#{self._id}\t bin is empty")
            pass

        self._bin.use_material()
        yield self._env.timeout(1)
        print(f"WS#{self._id}\tfinished\tt={self._env.now}")
        print("i")

