import simpy
import random as rd

from Factory import Factory
from ProductionLine import ProductionLine
from WorkStation import WorkStation

env = simpy.Environment()
factory = Factory(open_time=10, env=env)

prodLine1 = ProductionLine(id=1, env=env)

for i in range(6):
    prodLine1.add_work_station(WorkStation(id=i, env=env))

factory.add_production_line(prodLine1);

def alarm(env: simpy.Environment, delay: int, factory: Factory):
    yield env.timeout(delay)
    factory.action.interrupt()
    print("Alarm!")

env.process(alarm(env, 200, factory))
print("=== Simulation Started ===")
env.run(until=500)

print("=== Simulation Finished ===")
