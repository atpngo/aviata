#include "drone.hpp"
#include "camera_simulator.hpp" // temporary

int main(/*int argc, char** argv */)
{
    Target t;
    // t.lat = 2;
    //t.yaw = 180;

    Drone drone(t);
    drone.connect_gazebo();
    drone.arm();
    drone.takeoff();
    drone.initiate_docking(1);
    //drone.test2();

    return 0;
}