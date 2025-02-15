import simpy
import random as rd

from Factory import Factory
from ProductionLine import ProductionLine
from WorkStation import WorkStation

env = simpy.Environment()
Factory = Factory(env)

ProdLine1 = ProductionLine(env)

for i in range(6):
    ProdLine1.add_work_station(WorkStation(env))

Factory.add_production_line(ProdLine1)


print("=== Simulation Started ===")
env.run(until=500)
print("=== Simulation Finished ===")