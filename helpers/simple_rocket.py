
from math import pi
import numpy as np

def get_simple_rocket_change_equation_and_conditions(burn_time, thrust, fuel_mass, dry_mass, radius, drag_coefficient):

    # The rate the rocket loses mass due to fuel burn (assumes linear loss)
    fuel_mass_loss = fuel_mass / burn_time
    initial_mass = dry_mass + fuel_mass

    def rocket(x, t): #x is position, velocity and mass at time t

        old_position = x[0]
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

    return rocket, np.array([0, 0, initial_mass]) #initial position x, velocity, mass, angular velocity