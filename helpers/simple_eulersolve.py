from math import floor
import numpy as np

def eulersolve(func, t_initial, t_final, x_initial, dt):
    t = t_initial
    x = x_initial

    steps = floor((t_final-t_initial)/dt)

    tvec = np.zeros(steps)
    xvec = np.zeros( (steps, np.size(x_initial)))

    tvec[0] = t
    xvec[0] = x

    for i in range(1, steps):
        delta = dt*func(x, t)
        x = x + delta
        t = t + dt

        xvec[i] = x
        tvec[i] = t

    return tvec, xvec


def eulersolve_while_positive(func, t_initial, x_initial, dt):
    t = t_initial
    x = x_initial

    tvec = np.zeros((1, 1))
    xvec = np.zeros((1, np.shape(x)[0]))

    tvec[0] = t
    xvec[0] = x

    i = 0

    while x[0] >= 0:
        delta = dt*func(x, t, dt=dt)
        x = x + delta
        t = t + dt

        xvec = np.append(xvec, [x], 0)
        tvec = np.append(tvec, [t])
        
        i = i + 1

    return tvec, xvec



