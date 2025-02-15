import simpy

class WorkStation(object):
    def __init__(self, env: simpy.Environment) -> None:
        self._evn = env

    def process(self) -> simpy.Process:
        yield self._env.timeout(1)
