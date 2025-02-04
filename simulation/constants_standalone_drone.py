#!/usr/bin/env python3

import numpy as np

name = "aviata_1"

g = 9.81 # m/s^2

# AVIATA CONSTANTS
Ct = 6.295 # [Newtons] (for 3S batteries)
Cm = Ct * 0.05 # Newton-meters of torque generated by a single rotor at max power
num_rotors = 6 # Number of rotors on a single drone
rotor_angle = 10 # Canted motor angle (degrees)
r = 0.550 / 2 # Distance of each rotor from the center the drone (meters)
num_drones = 1
max_missing_drones = 0

M_drone = 1.8 # mass of a single drone in kg

I_drone = np.array([[0.12, 0.0 , 0.0],
                    [0.0 , 0.12, 0.0],  # moment of inertia tensor of a single drone in kg*m^2
                    [0.0 , 0.0 , 0.13]])

drone_prop_height = 0.05 # vertical distance between a drone's propellers and its center of mass (meters)

# Control Constants
# PX4 Defaults:
P_pos = np.array([0.95, 0.95, 1.0]) # MPC_XY_P, MPC_Z_P

P_vel = np.array([1.8, 1.8, 4.0]) # MPC_XY_VEL_P_ACC, MPC_Z_VEL_P_ACC
I_vel = np.array([0.4, 0.4, 2.0]) # MPC_XY_VEL_I_ACC, MPC_Z_VEL_I_ACC
D_vel = np.array([0.2, 0.2, 0.0]) # MPC_XY_VEL_D_ACC, MPC_Z_VEL_D_ACC

P_att = np.array([6.5, 6.5, 2.8]) # MC_ROLL_P, MC_PITCH_P, MC_YAW_P

P_att_rate = np.array([6.492, 6.492, 2.906]) # MC_ROLLRATE_P, MC_PITCHRATE_P, MC_YAWRATE_P. Scaled due to mixer: np.array([0.15*43.28, 0.15*43.28, 0.2*14.53])
I_att_rate = np.array([8.656, 8.656, 1.453]) # MC_ROLLRATE_I, MC_PITCHRATE_I, MC_YAWRATE_I. Scaled due to mixer: np.array([0.2*43.28, 0.2*43.28, 0.1*14.53])
I_lim_att_rate = np.array([12.984, 12.984, 4.359]) # MC_RR_INT_LIM, MC_PR_INT_LIM, MC_YR_INT_LIM. Scaled due to mixer: np.array([0.3*43.28, 0.3*43.28, 0.3*14.53])
D_att_rate = np.array([0.12984, 0.12984, 0.0]) # MC_ROLLRATE_D, MC_PITCHRATE_D, MC_YAWRATE_D. Scaled due to mixer: np.array([0.003*43.28, 0.003*43.28, 0.0*14.53])
# To scale all at once: MC_ROLLRATE_K, MC_PITCHRATE_K, MC_YAWRATE_K
# Also relevant: MC_ROLLRATE_FF, MC_PITCHRATE_FF, MC_YAWRATE_FF

max_vel_hor = 12.0 # m/s MPC_XY_VEL_MAX, MPC_XY_CRUISE
max_vel_down = 1.0 # MPC_Z_VEL_MAX_DN
max_vel_up = 3.0 # MPC_Z_VEL_MAX_UP
# Also relevant: MPC_TKO_SPEED

max_acc_hor = 5.0 # m/s^2 MPC_ACC_HOR_MAX, MPC_ACC_HOR
max_acc_down = 3.0 # MPC_ACC_DOWN_MAX
max_acc_up = 4.0 # MPC_ACC_UP_MAX

max_att_rate = np.deg2rad(np.array([220.0, 220.0, 200.0])) # radians/s MC_ROLLRATE_MAX, MC_PITCHRATE_MAX, MC_YAWRATE_MAX, MPC_YAWRAUTO_MAX
