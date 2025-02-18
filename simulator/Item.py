import simpy
import random

class Item:
    def __init__(self, env: simpy.Environment) -> None:
        self._env = env
        self._start_time = self._env.now
        self._end_time = self._env.now
        self._current_stage = 0
        self._approved = random.randint(0,100) > 5

    def update_end_time(self) -> None:
        self._end_time = self._env.now

    def get_production_time(self) -> None:
        return self._end_time - self._start_time

    def next_stage(self) -> None:
        self._current_stage += 1

    def get_current_stage(self) -> int:
        return self._current_stage

    def is_approved(self) -> bool:
        return self._approved
