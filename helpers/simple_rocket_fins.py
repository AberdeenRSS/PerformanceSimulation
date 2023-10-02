
from math import pi, sin, cos, pow, atan2
import numpy as np

def get_simple_rocket_FINS_change_equation_and_conditions(burn_time, thrust, fuel_mass, dry_mass, radius, angle, radius_fins):

    # The rate the rocket loses mass due to fuel burn (assumes linear loss)
    fuel_mass_loss = fuel_mass / burn_time
    initial_mass = dry_mass + fuel_mass

    angle_radians = angle / 180 * pi

    r = radius       #radius of the rocket tube in meters - 0.049/2
    r_fins = radius_fins   #radius of the semi-circular fins in meters - 0.04
    density_air = 1
    r_F = r + 4*r_fins/(3*pi)   #centre of mass of a semicircle + radius of the rocket


    def rocket(x, t): #x is position, velocity and mass at time t

        old_position = x[0]
        old_velocity = x[1]
        mass = x[2]
        old_angular_acceleration = x[3]
        delta_mass = 0

        force = 0
        if t < burn_time:
            force = thrust
            delta_mass = -fuel_mass_loss

        angle_effective = angle_radians - (0 if old_angular_acceleration == 0 else atan2((old_angular_acceleration * radius), old_velocity))

        cp = 0.01 + (1.5-0.01)*((angle_effective/pi)*(180/90))       #cp constant for the drag force for the fins at an angle (approximated by mel)

        #F drag = Area of the fins * Cp * v^2 * rho * 0.5 * sin(angle) * no. of fins
        F_drag = (pi*r_fins*r_fins*0.5)*cp*old_velocity*old_velocity*density_air*0.5*sin(angle_effective)*3

        F_drag_x = sin(angle_effective) * F_drag
        F_drag_y = cos(angle_effective) * F_drag

        #resultant torque acting on the whole rocket
        torque = r_F * F_drag_x

        inertia = 0.5 * mass * r*r        #inertia vector, for a uniform cylinder: 0.5 * m * r^2


        air_resistance = pow(old_velocity, 2) * 1/2 * pow(radius, 2) * pi * cp

        air_resistance += F_drag_y    #air resistance plus drag from spinning

        if old_velocity > 0:
            force = force - air_resistance
        else:
            force = force + air_resistance

        acceleration = force/mass
        acceleration = acceleration - 9.81


        angular_acceleration = torque/inertia
        
        return np.array([old_velocity, acceleration, delta_mass, angular_acceleration])

    return rocket, np.array([0, 0, initial_mass, 0]) #initial position x, velocity, mass, angular velocity