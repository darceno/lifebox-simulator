"""
Here you can edit most of the variables that are used as parameters in the simulation. 

"""

# SIMULATION SETTINGS
WIDTH_SIZE, HEIGHT_SIZE = 1280, 720 # default = 1280, 720
FPS = 60 # default = 60
BG_COLOR = (16, 32, 42) # default = (16, 32, 42)
STARTING_POPULATION = 10 # default = 10
START_WITH_MUTATION = True # default = True
YEAR = 60 # default = 60

# ORGANISMS SETTINGS
ORGANISM_SCALING = 0.5 # default = 0.5
ORGANISM_RADIUS = 64 * ORGANISM_SCALING # default = 64 * ORGANISM_SCALING
COST_TO_REPRODUCE = 30 # default = 30
REPRODUCTION_SUCESS_RATE = 0.7 # default = 0.7
STARTING_SIZE = 7 # default = 7
SIZE_BY_GENE = 1 # default = 1
STARTING_COLOR = "white" # default = "white"
SPEED = 1 # default = 1
MUTATION_CHANCE = 0.5 # default = 0.5

# INFO DISPLAY SETTINGS
enable_info_display = True # default = True
font_size = 30 # default = 30
font_color = "white" # default = "white"
anti_aliasing = True # default = True
show_FPS = True # default = True
show_population = True # default = True
show_time = True # defatult = True

# DEBUG INFO SETTINGS
debug_font_size = 30 # default = 30
debug_font_color = "yellow" # default = "yellow"
debug_background_color = "black" # default = "black"