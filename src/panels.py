import arcade

from settings import *


def information_panel(time, speed, eco_energy, population):
    global time_line, speed_line, energy_line, population_line
    last_line_Y = 20
    start_x = 10
    start_y = last_line_Y

    time_info = (f"Simulation time: {round(time)} seconds")
    time_line = arcade.Text(time_info, start_x, start_y, arcade.color.WHITE, FONT_SIZE )

    start_y = last_line_Y + LINE_HEIGHT
    speed_info = (f"Simulation speed: {speed}x")
    speed_line = arcade.Text(speed_info, start_x, start_y, arcade.color.WHITE, FONT_SIZE)

    start_y = last_line_Y + LINE_HEIGHT * 2
    energy_info = (f"Energy avaliable: {eco_energy}")
    energy_line = arcade.Text(energy_info, start_x, start_y, arcade.color.WHITE, FONT_SIZE)
    
    start_y = last_line_Y + LINE_HEIGHT * 3
    population_info = (f"Population: {len(population)}")
    population_line = arcade.Text(population_info, start_x, start_y, arcade.color.WHITE, FONT_SIZE)
    last_line_Y = 20
    start_x = 10
    start_y = last_line_Y

def draw_information_panel():
    time_line.draw()
    speed_line.draw()
    energy_line.draw()
    population_line.draw()