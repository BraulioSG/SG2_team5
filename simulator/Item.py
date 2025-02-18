import simpy
import random

class Item:
    """ Class representation for an Item
    Attributes:
    - env
    - start_time
    - end_time
    - current_stage
    - approved

    Methods: 
    + update_end_time()
    + get_production_time()
    + next_stage()
    + get_current_stage()
    + is_approved()
    """
    def __init__(self, env: simpy.Environment) -> None:
        self._env = env
        self._start_time = self._env.now
        self._end_time = self._env.now
        self._current_stage = 0
        self._approved = random.random() * 100 > 5

    def update_end_time(self) -> None:
        """ updates the end time to Now """
        self._end_time = self._env.now

    def get_production_time(self) -> None:
        """ returns the delta time between end time and start time """
        return self._end_time - self._start_time

    def next_stage(self) -> None:
        """ moves the item to the next stage """ 
        self._current_stage += 1

    def get_current_stage(self) -> int:
        return self._current_stage

    def is_approved(self) -> bool:
        return self._approved
