# PX4 parameter configuration. See https://docs.px4.io/v1.11/en/advanced_config/parameter_reference.html for documentation.
# Lines should be <= 128 characters

###############################
### UNIVERSAL AVIATA PARAMS ###
###############################

# param set MAV_SYS_ID 1 # Set to unique ID on each drone for multi-drone tests

# Safety checks / failsafes
param set CBRK_IO_SAFETY 22027
param set COM_POWER_COUNT 0

# Ports config
param set MAV_1_CONFIG 102 # Use TELEM 2 for RPi

# Airframe config
param set MAV_TYPE 13 # Hexarotor
param set GPS_UBX_DYNMODEL 6 # Default for multicopters


#################################
### HARDWARE DEPENDENT PARAMS ###
#################################

param set SYS_AUTOSTART 6003 # Use 6003 for custom hex airframe with AUX outputs. For normal hex, use 6001.

# Battery configuration (TODO configure for 4 drone test)
param set BAT1_A_PER_V 15.391030311584473
param set BAT1_N_CELLS 3
param set BAT1_V_DIV 10.177939414978027
param set BAT_A_PER_V 15.391030311584473
param set BAT_N_CELLS 3
param set BAT_V_DIV 10.177939414978027

# Rangefinder config (TODO configure for 4 drone test)
param set SENS_TFMINI_CFG 104 # Serial 4
param set EKF2_RNG_AID 1
param set EKF2_RNG_POS_X 0.0 # X position of range finder origin in body frame 
    # (forward axis with origin relative to vehicle center of gravity)
param set EKF2_RNG_POS_Y 0.578 # Y position of range finder origin in body frame 
    # (right axis with origin relative to vehicle center of gravity)
param set EKF2_RNG_POS_Z 0.0 # Z position of range finder origin in body frame 
    # (down axis with origin relative to vehicle center of gravity)

# PWM min and max
param set PWM_MIN 1100
param set PWM_MAX 2000
param set PWM_AUX_MIN 1100
param set PWM_AUX_MAX 2000

# Other PWM config
param set PWM_RATE 400
param set PWM_AUX_DISARMED 900
param set PWM_AUX_RATE 400


#############################
### USER DEPENDENT PARAMS ###
#############################

# Safety checks / failsafes
param set COM_DISARM_PRFLT 0.0 # Don't auto disarm before taking off
param set COM_OBL_ACT 4 # Lockdown on offboard loss (no RC)
param set COM_OBL_RC_ACT 7 # Lockdown on offboard loss (with RC)
param set COM_OF_LOSS_T 0.5 # Offboard loss failsafe timeout (seconds)
param set COM_RC_OVERRIDE 3 # Enable RC override in auto and offboard
param set NAV_RCL_ACT 3 # Land on RC loss

# Miscellaneous flight config
param set MIS_TAKEOFF_ALT 1.0 # (meters)
param set MPC_MAN_TILT_MAX 20.0 # Max tilt angle in Manual or Altitude mode
param set NAV_ACC_RAD 2.0 # Waypoint acceptance radius (meters)
param set RTL_DESCEND_ALT 10.0
param set RTL_RETURN_ALT 30.0
param set RTL_LAND_DELAY 0.0

# RC controller flight modes (set to Manual, Altitude, Position for 3-position switch)
param set COM_FLTMODE1 0
param set COM_FLTMODE4 1
param set COM_FLTMODE6 2

# Calibration and config for Ryan's RC controller
param set RC1_MAX 2001.0
param set RC1_TRIM 1501.0
param set RC3_TRIM 1000.0
param set RC4_DZ 100.0
param set RC4_MAX 1996.0
param set RC5_MAX 2001.0
param set RC7_MAX 2001.0
param set RC_CHAN_CNT 8
param set RC_MAP_ARM_SW 5
param set RC_MAP_FLTMODE 7
param set RC_MAP_KILL_SW 8
param set RC_MAP_PITCH 2
param set RC_MAP_ROLL 1
param set RC_MAP_THROTTLE 3
param set RC_MAP_YAW 4

# Controller Tuning
param set IMU_DGYRO_CUTOFF 20.0
param set IMU_GYRO_CUTOFF 30.0

param set MPC_XY_P 0.513

param set MPC_XY_VEL_P_ACC 1.215
param set MPC_XY_VEL_I_ACC 0.135
param set MPC_XY_VEL_D_ACC 0.135

param set MC_ROLL_P 4.3875
param set MC_PITCH_P 4.3875
param set MC_YAW_P 1.5679999999999998

param set MC_ROLLRATE_P 4.869
param set MC_ROLLRATE_I 3.2460000000000004
param set MC_RR_INT_LIM 4.869
param set MC_ROLLRATE_D 0.073035
param set MC_PITCHRATE_P 4.869
param set MC_PITCHRATE_I 3.2460000000000004
param set MC_PR_INT_LIM 4.869
param set MC_PITCHRATE_D 0.073035
param set MC_YAWRATE_P 2.0342
param set MC_YAWRATE_I 0.50855
param set MC_YR_INT_LIM 1.52565
param set MC_YAWRATE_D 0.0
