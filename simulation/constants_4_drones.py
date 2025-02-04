#!/usr/bin/env python3

import numpy as np

name = "aviata_4"

g = 9.81 # m/s^2

# AVIATA CONSTANTS
motor_battery_voltage_scaling = 12.8 / 16 # Motor specs are given for 16V, but voltage could drop lower than that. Absolute worst-case is 12.8V. (https://www.amazon.com/SoloGood-Brushless-T-Motor-AIR2216-Propeller/dp/B085C8D6YT)
Ct = 1.293 * g * motor_battery_voltage_scaling # Newtons of force generated by a single rotor at max power (6.295 N for 3S batteries)
Cm = 0.18 * motor_battery_voltage_scaling # Newton-meters of torque generated by a single rotor at max power
num_rotors = 6 # Number of rotors on a single drone
rotor_angle = 10 # Canted motor angle (degrees)
r = 0.550 / 2 # Distance of each rotor from the center the drone (meters)
R = 1.193 # Distance between the center of a drone and the center of the structure (meters)
num_drones = 4 # Maximum number of drones on the structure
max_missing_drones = 0 # Maximum number of drones that are allowed to be missing from the structure
drones_face_inward = False # True if the front of each drone faces inward when docked, False if they face outward

M_drone = 1.562 + 0.518 # mass of a single drone in kg (drone + battery)
M_structure = 0.360 + 0.784 # mass of the structure in kg (hub + carbon fiber). 4.1771 kg for full frame (but that might be outdated)
M_payload = 0 # mass of the payload in kg (5 lb payload = 2.26796 kg)
M_structure_payload = M_structure + M_payload

I_drone = np.array([[0.0, 0.0, 0.0],
                    [0.0, 0.0, 0.0],  # TODO moment of inertia tensor of a single drone in kg*m^2
                    [0.0, 0.0, 0.0]])

# For 4-drone frame, calculated based on the 4 carbon fiber tubes:
I_structure = np.array([[0.186, 0.0  , 0.0  ],
                        [0.0  , 0.186, 0.0  ],  # moment of inertia tensor of the structure in kg*m^2
                        [0.0  , 0.0  , 0.372]])

# # For 8-drone frame (might be outdated):
# I_structure = np.array([[1.3958, 0.0   , 0.0   ],
#                         [0.0   , 1.3958, 0.0   ],  # moment of inertia tensor of the structure in kg*m^2
#                         [0.0   , 0.0   , 2.7902]])

I_payload = np.array([[0.0, 0.0, 0.0],
                      [0.0, 0.0, 0.0],  # TODO moment of inertia tensor of the payload in kg*m^2
                      [0.0, 0.0, 0.0]])

I_structure_payload = I_structure + I_payload

payload_structure_height = 0 # TODO vertical distance between the structure center of mass and payload center of mass (meters)
structure_drone_height = 0.06 # vertical distance between a drone's center of mass and the structure center of mass (meters)
structpayload_drone_height = (M_structure * structure_drone_height + M_payload * (payload_structure_height + structure_drone_height)) / M_structure_payload  # vertical distance between a drone's center of mass and the structure+payload center of mass (meters)
drone_prop_height = 0.047 # vertical distance between a drone's propellers and its center of mass (meters)
docking_attachment_offset = 0.06 # vertical distance between a drone's propellers and the approximate center of the docking attachment (meters)

# Control Constants
rollrate_pitchrate_scale = 0.75
yawrate_scale = 0.65
rate_derivative_scale = 0.75
rate_integral_scale = 0.5
roll_pitch_scale = rollrate_pitchrate_scale * 0.9
yaw_scale = yawrate_scale * 0.75
xy_vel_scale = roll_pitch_scale
xy_vel_integral_scale = 0.5
xy_pos_scale = xy_vel_scale * 0.8

P_pos = np.array([0.95*xy_pos_scale, 0.95*xy_pos_scale, 1.0]) # MPC_XY_P, MPC_Z_P

P_vel = np.array([1.8*xy_vel_scale, 1.8*xy_vel_scale, 4.0]) # MPC_XY_VEL_P_ACC, MPC_Z_VEL_P_ACC
I_vel = np.array([0.4*xy_vel_scale*xy_vel_integral_scale, 0.4*xy_vel_scale*xy_vel_integral_scale, 2.0]) # MPC_XY_VEL_I_ACC, MPC_Z_VEL_I_ACC
D_vel = np.array([0.2*xy_vel_scale, 0.2*xy_vel_scale, 0.0]) # MPC_XY_VEL_D_ACC, MPC_Z_VEL_D_ACC

P_att = np.array([6.5*roll_pitch_scale, 6.5*roll_pitch_scale, 2.8*yaw_scale]) # MC_ROLL_P, MC_PITCH_P, MC_YAW_P

P_att_rate = np.array([6.492*rollrate_pitchrate_scale, 6.492*rollrate_pitchrate_scale, 2.906*yawrate_scale]) # MC_ROLLRATE_P, MC_PITCHRATE_P, MC_YAWRATE_P
I_att_rate = np.array([8.656*rollrate_pitchrate_scale, 8.656*rollrate_pitchrate_scale, 1.453*yawrate_scale])*rate_integral_scale # MC_ROLLRATE_I, MC_PITCHRATE_I, MC_YAWRATE_I
I_lim_att_rate = np.array([12.984*rollrate_pitchrate_scale, 12.984*rollrate_pitchrate_scale, 4.359*yawrate_scale])*rate_integral_scale # MC_RR_INT_LIM, MC_PR_INT_LIM, MC_YR_INT_LIM
D_att_rate = np.array([0.12984*rollrate_pitchrate_scale, 0.12984*rollrate_pitchrate_scale, 0.0*yawrate_scale])*rate_derivative_scale # MC_ROLLRATE_D, MC_PITCHRATE_D, MC_YAWRATE_D
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

if __name__ == '__main__':
    print("param set MPC_XY_P", P_pos[0])
    print()
    print("param set MPC_XY_VEL_P_ACC", P_vel[0])
    print("param set MPC_XY_VEL_I_ACC", I_vel[0])
    print("param set MPC_XY_VEL_D_ACC", D_vel[0])
    print()
    print("param set MC_ROLL_P", P_att[0])
    print("param set MC_PITCH_P", P_att[1])
    print("param set MC_YAW_P", P_att[2])
    print()
    print("param set MC_ROLLRATE_P", P_att_rate[0])
    print("param set MC_ROLLRATE_I", I_att_rate[0])
    print("param set MC_RR_INT_LIM", I_lim_att_rate[0])
    print("param set MC_ROLLRATE_D", D_att_rate[0])
    print("param set MC_PITCHRATE_P", P_att_rate[1])
    print("param set MC_PITCHRATE_I", I_att_rate[1])
    print("param set MC_PR_INT_LIM", I_lim_att_rate[1])
    print("param set MC_PITCHRATE_D", D_att_rate[1])
    print("param set MC_YAWRATE_P", P_att_rate[2])
    print("param set MC_YAWRATE_I", I_att_rate[2])
    print("param set MC_YR_INT_LIM", I_lim_att_rate[2])
    print("param set MC_YAWRATE_D", D_att_rate[2])

# PX4 Defaults:
# P_pos = np.array([0.95, 0.95, 1.0]) # MPC_XY_P, MPC_Z_P

# P_vel = np.array([1.8, 1.8, 4.0]) # MPC_XY_VEL_P_ACC, MPC_Z_VEL_P_ACC
# I_vel = np.array([0.4, 0.4, 2.0]) # MPC_XY_VEL_I_ACC, MPC_Z_VEL_I_ACC
# D_vel = np.array([0.2, 0.2, 0.0]) # MPC_XY_VEL_D_ACC, MPC_Z_VEL_D_ACC

# P_att = np.array([6.5, 6.5, 2.8]) # MC_ROLL_P, MC_PITCH_P, MC_YAW_P

# P_att_rate = np.array([6.492, 6.492, 2.906]) # MC_ROLLRATE_P, MC_PITCHRATE_P, MC_YAWRATE_P. Scaled due to mixer: np.array([0.15*43.28, 0.15*43.28, 0.2*14.53])
# I_att_rate = np.array([8.656, 8.656, 1.453]) # MC_ROLLRATE_I, MC_PITCHRATE_I, MC_YAWRATE_I. Scaled due to mixer: np.array([0.2*43.28, 0.2*43.28, 0.1*14.53])
# I_lim_att_rate = np.array([12.984, 12.984, 4.359]) # MC_RR_INT_LIM, MC_PR_INT_LIM, MC_YR_INT_LIM. Scaled due to mixer: np.array([0.3*43.28, 0.3*43.28, 0.3*14.53])
# D_att_rate = np.array([0.12984, 0.12984, 0.0]) # MC_ROLLRATE_D, MC_PITCHRATE_D, MC_YAWRATE_D. Scaled due to mixer: np.array([0.003*43.28, 0.003*43.28, 0.0*14.53])
# # To scale all at once: MC_ROLLRATE_K, MC_PITCHRATE_K, MC_YAWRATE_K
# # Also relevant: MC_ROLLRATE_FF, MC_PITCHRATE_FF, MC_YAWRATE_FF

# max_vel_hor = 12.0 # m/s MPC_XY_VEL_MAX, MPC_XY_CRUISE
# max_vel_down = 1.0 # MPC_Z_VEL_MAX_DN
# max_vel_up = 3.0 # MPC_Z_VEL_MAX_UP
# # Also relevant: MPC_TKO_SPEED

# max_acc_hor = 5.0 # m/s^2 MPC_ACC_HOR_MAX, MPC_ACC_HOR
# max_acc_down = 3.0 # MPC_ACC_DOWN_MAX
# max_acc_up = 4.0 # MPC_ACC_UP_MAX

# max_att_rate = np.deg2rad(np.array([220.0, 220.0, 200.0])) # radians/s MC_ROLLRATE_MAX, MC_PITCHRATE_MAX, MC_YAWRATE_MAX, MPC_YAWRAUTO_MAX
