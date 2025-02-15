import simpy

class Factory(object):
    def __init__(self, env: simpy.Environment):
        self._env = env

    def process(self) -> simpy.Process:
        yield self._env.timeout(1)
