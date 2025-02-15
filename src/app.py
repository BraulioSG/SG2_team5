import simpy
import random as rd

from Factory import Factory
from ProductionLine import ProductionLine
from WorkStation import WorkStation

env = simpy.Environment()
Factory = Factory(env)
env.run(until=50)
