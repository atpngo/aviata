#!/usr/bin/env python

import numpy as np
import px4_mixer_multirotor
import generate_matrices
import constants
import graphics
from drones import *


def mixer_test():
    missing_drones = [] # 0 through 7
    geometry, geometries = generate_matrices.generate_aviata_matrices(missing_drones)
    mixer = geometry['mix']['B_px_4dof']
    actuator_effectiveness = geometry['mix']['A_4dof']

    setpoint = np.matrix([0, 0, 0, 0.5]).T
    print("normalized forces (used by PX4):")
    print(setpoint)
    print()

    ideal_forces = np.linalg.multi_dot([actuator_effectiveness, mixer, setpoint])
    print("ideal forces:")
    print(ideal_forces)
    print()

    u, u_final = px4_mixer_multirotor.normal_mode(setpoint, mixer, 0.0, 1.0)

    print("motor inputs (used by PX4):")
    print(u_final)
    print()

    actual_forces = np.dot(actuator_effectiveness, u_final)
    print("actual forces:")
    print(actual_forces)
    print()


def const_forces_test():
    missing_drones = [] # 0 through 7
    sample_period_ms = 50
    forces_setpoint = np.matrix([0.0007, 0.0, 0.2, 0.59]).T

    world = PhysicalWorld(constants.num_drones, sample_period_ms)
    world.set_missing_drones(missing_drones)
    world.network.broadcast(Drone.set_forces_setpoint, forces_setpoint)

    def loop(GraphicsState):
        nonlocal world
        world.tick()
        GraphicsState.pos = world.structure.pos
        GraphicsState.att = world.structure.att
        GraphicsState.rotors = world.structure.geometry['rotors']
        GraphicsState.motor_inputs = world.structure.u

    graphics.main(loop, world.sample_period_ms)


if __name__ == '__main__':
    const_forces_test()