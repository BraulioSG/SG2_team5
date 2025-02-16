import simpy

from Resuppliers import SuppliersContainer

class _Bin:
    """
    Represents the Bin for a workStation
    Attributes: 
    - material_units
    - capacity

    Methods:
    + use_material() -> None
    + resupply() -> None
    + get_remaining_units() -> int
    + is_empty() -> bool
    """
    def __init__(self, capacity: int = 25):
        self._material_units = capacity
        self._capacity = capacity

    def use_material(self):
        """ Decrease by one the material units, if is empty it will rise an exception """
        if(self.is_empty()):
            #raise Exception("Try to use material when the bin is empty")
            print("bin is empty")
            return
        self._material_units -= 1

    def resupply(self) -> None:
        """ Sets the material units to the same value as the capacity """
        self._material_units = self._capacity

    def get_remaining_units(self) -> int:
        """ Returns the number of material units remaining in the bin """
        return self._material_units

    def is_empty(self) -> bool:
        """ Returns true if the material units is less or equal to zero"""
        return self.get_remaining_units() <= 0

class WorkStation(object):
    def __init__(self, id: int, env: simpy.Environment) -> None:
        self._env = env
        self._bin = _Bin()
        self._id = id

    def set_suppliers(self, suppliers: SuppliersContainer) -> None:
        self._suppliers = suppliers


    def work(self) -> simpy.Process:
        #print(f"WS#{self._id}\tstarted \tt={self._env.now}\tu={self._bin.get_remaining_units()}")
        if(self._bin.is_empty()):
            yield self._env.process(self.resupply())

        self._bin.use_material()
        yield self._env.timeout(1)
        #print(f"WS#{self._id}\tfinished\tt={self._env.now}\tu={self._bin.get_remaining_units()}")

    def resupply(self) -> simpy.Process:
        supplier = self._suppliers.check_for_available()
        while supplier == False:
            #print(f"WS#{self._id}\twaiting for supply \tt={self._env.now}")
            try:
                suplier = self._suppliers.check_for_available()
            except simpy.Interruption:
                return

        #print(f"WS#{self._id}\tsupplying \tt={self._env.now}")
        yield self._env.process(supplier.resupply())
        self._bin.resupply()
