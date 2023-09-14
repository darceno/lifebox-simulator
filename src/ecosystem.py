import time

from settings import *

class Ecosystem():
    
    def __init__(self):        
        self.last_energy_update = 0
        self.energy_avaliable = 100

    def energy_updade(self):
        if time.time() - self.last_energy_update > 1:
            self.energy_avaliable += ENERGY_PRODUCTION
            self.last_energy_update = time.time()
            print("oi")
