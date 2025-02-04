import math

class PIDController:
    def __init__(self, dt):
        self.dt = dt
        self.prev_errs = (0, 0, 0)
        self.sum_errs = (0, 0, 0)
        self.ki_dv_start = False
        self.ki_ev_start = False
        self.ki_nv_start = False

    def get_velocities(self, x_err, y_err, alt_err, max_speed):
        ku_nv = 2.6
        ku_ev = 2.15
        ku_dv = 3.5

        # tu_nv = 0.75
        # tu_ev = 0.90
        # tu_dv = 0.45

        # Ziegler-Nichols classic PID
        kp_nv = 0.6 * ku_nv 
        kp_ev = 0.6 * ku_ev
        kp_dv = 0.6 * ku_dv

        # ZN: 0.075 * ku_nv * tu_nv, + minor manual tuning
        kd_nv = 0.15 
        kd_ev = 0.15
        kd_dv = 0.12

        # manual tuning
        # ki_nv = 0 
        # ki_ev = 0 #0.16 
        # ki_dv = 0 #9.3

        east_velocity = x_err * kp_ev + (x_err - self.prev_errs[0]) / self.dt * kd_ev #+ self.sum_errs[0] * self.dt * ki_ev
        north_velocity = y_err * kp_nv + (y_err - self.prev_errs[1]) / self.dt * kd_nv #+ self.sum_errs[1] * self.dt * ki_nv
        down_velocity = alt_err * kp_dv + (alt_err - self.prev_errs[2]) / self.dt * kd_dv #+ self.sum_errs[2] * self.dt * ki_dv

        # Cap maximum speed
        down_velocity = self.abs_min(down_velocity, max_speed)
        # east_velocity = self.abs_min(east_velocity, self.abs_min(down_velocity, max_speed))
        # north_velocity = self.abs_min(north_velocity, self.abs_min(down_velocity, max_speed))

        # if alt_err < 0.5:
        #     self.ki_dv_start = True
        # if x_err < 0.5:
        #     self.ki_ev_start = True
        # if y_err < 0.5:
        #     self.ki_nv_start = True

        self.prev_errs = (x_err, y_err, alt_err)
        # self.sum_errs = (
        #                     self.sum_errs[0] + x_err if self.ki_ev_start is True else 0, 
        #                     self.sum_errs[1] + y_err if self.ki_nv_start is True else 0, 
        #                     self.sum_errs[2] + alt_err if self.ki_dv_start is True else 0
        #                 )

        return (east_velocity, north_velocity, down_velocity)

    def abs_min(self, val, cap):
        sign = (val / abs(val)) if val != 0 else 1
        return min(abs(val), cap) * sign