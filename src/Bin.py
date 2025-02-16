class Bin:
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
            raise Exception("Try to use material when the bin is empty")
            return
        self._material_units -= 1

    def refill(self) -> None:
        """ Sets the material units to the same value as the capacity """
        self._material_units = self._capacity

    def get_remaining_units(self) -> int:
        """ Returns the number of material units remaining in the bin """
        return self._material_units

    def is_empty(self) -> bool:
        """ Returns true if the material units is less or equal to zero"""
        return self.get_remaining_units() <= 0


