import os
import simpy
import random as rd

from Factory import Factory
from ProductionLine import ProductionLine
from Reporter import Reporter

os.system('color')
env = simpy.Environment()

factory = Factory(env)
factory.add_production_line([0.02, 0.01, 0.05, 0.15, 0.07, 0.06])

def alarm(env: simpy.Environment, delay: int, factory: Factory):
    yield env.timeout(delay)
    factory.action.interrupt()
    print("Alarm!")


factory.start()
env.process(alarm(env, 5000, factory))
print("=== Simulation Started ===")
env.run(until=5000)

print("=== Simulation Finished ===")

reporter = Reporter(factory)
factory.print_report()
