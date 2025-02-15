import simpy
import random as rd

from Factory import Factory

env = simpy.Environment()
Factory = Factory(env)
env.run(until=50)
