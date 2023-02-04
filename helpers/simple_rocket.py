
from math import cos, pi, sin, sqrt
import numpy as np

def get_simple_rocket_change_equation_and_conditions(burn_time, thrust, fuel_mass, dry_mass, radius, drag_coefficient):

    # The rate the rocket loses mass due to fuel burn (assumes linear loss)
    fuel_mass_loss = fuel_mass / burn_time
    initial_mass = dry_mass + fuel_mass

    def rocket(x, t):

        old_velocity = x[1]
        mass = x[2]
        delta_mass = 0

        force = 0
        if t < burn_time:
            force = thrust
            delta_mass = -fuel_mass_loss

        air_resistance = pow(old_velocity, 2) * 1/2 * pow(radius, 2) * pi * drag_coefficient

        if old_velocity > 0:
            force = force - air_resistance
        else:
            force = force + air_resistance

        a = force/mass
        a = a - 9.81


        v = a
        x = x[1]
        
        return np.array([x, v, delta_mass])

    return rocket, np.array([0, 0, initial_mass])

def get_simple_rocket_change_equation_and_conditions_angled(burn_time, thrust, fuel_mass, dry_mass, radius, drag_coefficient, angle):

    # The rate the rocket loses mass due to fuel burn (assumes linear loss)
    fuel_mass_loss = fuel_mass / burn_time
    initial_mass = dry_mass + fuel_mass

    def rocket(x, t):

        old_position_x = x[0]
        old_position_y = x[1]
        old_velocity_x = x[2]
        old_velocity_y = x[3]

        old_velocity = sqrt(pow(old_velocity_x, 2) + pow(old_velocity_y, 2))

        mass = x[4]
        delta_mass = 0

        force = 0
        if t < burn_time:
            force = thrust
            delta_mass = -fuel_mass_loss

        air_resistance = pow(old_velocity, 2) * 1/2 * pow(radius, 2) * pi * drag_coefficient

        if old_velocity > 0:
            force = force - air_resistance
        else:
            force = force + air_resistance

        acceleration   = force/mass
        acceleration_x = sin(angle) * acceleration
        acceleration_y = cos(angle) * acceleration

        acceleration_y = acceleration_y - 9.81

        velocity_x = acceleration_x
        velocity_y = acceleration_y

        position_x = old_velocity_x
        position_y = old_velocity_y
         
        return np.array([position_x, position_y, velocity_x, velocity_y, delta_mass])

    return rocket, np.array([0, 0, 0, 0, initial_mass])
