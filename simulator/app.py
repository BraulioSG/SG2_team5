import os
import simpy
import random as rd

from Factory import Factory
from Reporter import Reporter

os.system('color')

class App:
    def __init__(self):
        self.env = simpy.Environment()
        self.factory = Factory(self.env, self)
        self.factory.add_production_line([0.02, 0.01, 0.05, 0.15, 0.07, 0.06])

    def start(self, delay):
        self.factory.start()
        self.env.process(self.wait_for_end(delay))
        #print("=== Simulation Started ===")
        self.env.run(until=5000)
        #print("=== Simulation Finished ===")

        #self.factory.print_report()
        self.factory.print_for_csv()

    def wait_for_end(self, delay):
        yield self.env.timeout(delay)
        action = self.factory.get_action()
        if action and action.is_alive:
            action.interrupt()

    def alarm(self):
        action = self.factory.get_action()
        if action and action.is_alive:
            action.interrupt()
        #print("ALARM!!")

app = App()
app.start(5000)
