
from dataclasses import dataclass
from itertools import islice
from math import pi, sin, cos, pow, atan2
from typing import Iterable
import numpy as np

class Mach24Fin:

    def calc_fin_area(self) -> int:
        return 0
    
    def calc_fin_center_mass(self) -> int:
        return 0

@dataclass
class CircularMach24Fin(Mach24Fin):

    radius_fins: float = 0
    '''Radius of the fins in m'''

    def calc_fin_area(self):
        return pi*self.radius_fins*self.radius_fins*0.5
    
    def calc_fin_center_mass(self):
        return 4*self.radius_fins/(3*pi)

@dataclass
class Mach24Stage:

    burn_time: float = 0
    '''Burn time of the stage (s)'''

    thrust: float = 0
    '''Thrust in Newton'''

    fuel_mass: float = 0
    '''Fuel mass in kg'''

    dry_mass: float = 0
    '''Dry mass in kg'''

    radius: float = 0
    '''Radius of the rocket body in m '''

    ignition_delay: float = 0
    '''Delay of ignition after last stage fired'''

    stage_delay: float = 0
    '''Time after motor has burned out until staging'''

    fin: Mach24Fin | None = None
    '''Fin used by the rocket'''

    def fuel_mass_loss(self) -> float:
        return self.fuel_mass / self.burn_time


def get_mach_24_rocket(stages: list[Mach24Stage], launch_angle: float, drag_coefficient: float):

    angle_radians = launch_angle / 180 * pi
    density_air = 1

    # The total initial mass of the rocket
    initial_mass = sum([s.dry_mass + s.fuel_mass for s in stages])

    # r_F = r + 4*r_fins/(3*pi)   #centre of mass of a semicircle + radius of the rocket

    cur_stage_index = -1

    cur_stage_burn_start = 0
    cur_stage_burn_end = 0
    next_stage_time = 0
    cur_stage_fin_torque_point = 0
    cur_inertia = 0

    def stage(time: float):
        '''Stage the rocket'''

        nonlocal cur_stage_index
        nonlocal cur_stage_burn_start
        nonlocal next_stage_time
        nonlocal cur_stage_burn_end
        nonlocal cur_stage_fin_torque_point
        nonlocal cur_inertia

        cur_stage_index = cur_stage_index + 1
        cur_stage = stages[cur_stage_index]

        cur_stage_burn_start = time + cur_stage.ignition_delay
        cur_stage_burn_end = time + cur_stage.burn_time + cur_stage.ignition_delay

        next_stage_time = time + cur_stage.ignition_delay + cur_stage.burn_time + cur_stage.stage_delay

        cur_stage_fin_torque_point = cur_stage.radius + cur_stage.fin.calc_fin_center_mass()

        cur_inertia = sum([ 0.5 * (s.dry_mass + s.fuel_mass/2) * s.radius * s.radius for s in islice(stages, cur_stage_index, None)]) # Approximation (no mass loss considered)

        return 0 if cur_stage_index < 1 else stages[cur_stage_index-1].dry_mass

    stage(0)

    def rocket(x, t, **kwargs): #x is position, velocity and mass at time t

        dt = kwargs['dt']

        cur_stage = stages[cur_stage_index]
        delta_mass = 0

        if t > next_stage_time and (cur_stage_index + 1) < len(stages):
            delta_mass -= stage(t)*(1/dt)
            cur_stage = stages[cur_stage_index]

        old_position = x[0]
        old_velocity = x[1]
        mass = x[2]
        old_angular_acceleration = x[3]

        force = 0

        if t >= cur_stage_burn_start and t < cur_stage_burn_end:
            force = cur_stage.thrust
            delta_mass -= cur_stage.fuel_mass_loss()

        angle_effective = angle_radians - (0 if old_angular_acceleration == 0 else atan2((old_angular_acceleration * cur_stage.radius), old_velocity))

        cp = 0.01 + (1.5-0.01)*((angle_effective/pi)*(180/90))       #cp constant for the drag force for the fins at an angle (approximated by mel)

        #F drag = Area of the fins * Cp * v^2 * rho * 0.5 * sin(angle) * no. of fins
        F_drag = cur_stage.fin.calc_fin_area()*cp*old_velocity*old_velocity*density_air*0.5*sin(angle_effective)*3

        F_drag_x = sin(angle_effective) * F_drag
        F_drag_y = cos(angle_effective) * F_drag

        #resultant torque acting on the whole rocket
        torque = cur_stage_fin_torque_point* F_drag_x
       #inertia vector, for a uniform cylinder: 0.5 * m * r^2

        air_resistance = pow(old_velocity, 2) * 1/2 * pow(cur_stage.radius, 2) * pi * drag_coefficient

        air_resistance += F_drag_y    #air resistance plus drag from spinning

        if old_velocity > 0:
            force = force - air_resistance
        else:
            force = force + air_resistance

        acceleration = force/mass
        acceleration = acceleration - 9.81

        angular_acceleration = torque/cur_inertia
        
        return np.array([old_velocity, acceleration, delta_mass, angular_acceleration])

    return rocket, np.array([0, 0, initial_mass, 0]) #initial position x, velocity, mass, angular velocity