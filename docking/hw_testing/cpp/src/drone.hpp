#ifndef DRONE_H_
#define DRONE_H_

#define MAX_ATTEMPTS 3
#define MAX_HEIGHT 3
#define MAX_HEIGHT_STAGE_2 10
#define STAGE_1_TOLERANCE 0.10
#define STAGE_2_TOLERANCE 0.05

#include "raspi_camera.hpp"
#include <mavsdk/mavsdk.h>

using namespace mavsdk;

class Drone {

public: 
    Drone(Target t);
    bool connect_gazebo();
    bool takeoff();
    void initiate_docking(int target_id);

private:
    Mavsdk mavsdk;
    RaspiCamera raspi_camera;
    // ImageAnalyzer image_analyzer; 
    float m_north;
    float m_east;
    float m_down;
    float m_yaw;
    Target m_target_info;
    float m_dt; // loop cycle time, seconds

    std::shared_ptr<mavsdk::System> m_system; // pointer to mavsdk connection to drone

    void set_position(float n, float e, float d); // set position obtained from telemetry
    void set_yaw(float yaw); // set yaw angle obtained from telemetry

    bool stage1(int target_id);
    void stage2(int target_id);
    void offset_errors(double x, double y, double alt, double rot, int target_id); // offset for stg 1->2 transition
    void safe_land();
    void land();
};


#endif // DRONE_H_