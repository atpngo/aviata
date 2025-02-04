#ifndef PID_H
#define PID_H

#include <array>
#include "util.hpp"
class Velocities;

//PID Controller class
class PIDController
{
public:
    PIDController(bool overshoot = false);
    ~PIDController();
    Velocities getVelocities(float x_err, float y_err, float alt_err, float rot_err, float max_speed);

private:
    float m_dt;
    bool m_overshoot_adjust;
    Errors m_prev_errs;
};
#endif //PID_H