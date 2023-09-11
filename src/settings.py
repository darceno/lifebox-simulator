"""
Here you can edit most of the variables that are used as parameters in the simulation. 

"""

# SIMULATION SETTINGS
WIDTH_SIZE, HEIGHT_SIZE = 1280, 720 # default = 1280, 720
BG_COLOR = (16, 32, 42) # default = (16, 32, 42)
STARTING_POPULATION = 10 # default = 10
START_WITH_MUTATION = True # default = True
YEAR = 60 # default = 60

# ECOSYSTEM SETTINGS
ENERGY_PRODUCTION = 100 # default = 100

# ORGANISMS SETTINGS
ORGANISM_SCALING = 0.5 # default = 0.5
ORGANISM_RADIUS = 64 * ORGANISM_SCALING # default = 64 * ORGANISM_SCALING
COST_TO_REPRODUCE = 30 # default = 30
REPRODUCTION_SUCESS_RATE = 0.7 # default = 0.7
MUTATION_CHANCE = 0.5 # default = 0.5