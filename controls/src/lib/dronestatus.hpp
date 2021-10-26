#ifndef DRONESTATUS_HPP
#define DRONESTATUS_HPP

#include "pid_controller.hpp"
#include <opencv2/core.hpp>
#include <opencv2/core/types.hpp>
#include <opencv2/imgcodecs.hpp>
#include <mavsdk/mavsdk.h>
#include <mavsdk/plugins/telemetry/telemetry.h>
#include <mavsdk/plugins/action/action.h>
#include <mavsdk/plugins/offboard/offboard.h>
#include <mavsdk/geometry.h>

struct DroneSettings {
    bool sim;
    bool modify_px4_mixers;
    uint8_t n_docking_slots;
    uint8_t max_missing_drones;
};

enum DroneState {
    STANDBY,
    ARRIVING, // AKA Docking Stage 0
    DOCKING_STAGE_1,
    DOCKING_STAGE_2,
    DOCKED_FOLLOWER,
    DOCKED_LEADER,
    UNDOCKING,
    DEPARTING,
    NEEDS_SERVICE
};

struct DroneStatus {
// struct DroneStatus_Docked { // update naming convention?
    std::string drone_id;
    std::string ip_address {""};
    uint8_t mavlink_sys_id {0};
    DroneState drone_state;
    int8_t docking_slot;

    float battery_percent {0}; 
    float gps_position[4] {0};
    float yaw {0};
};

// struct DroneStatus_Attitude {
//     std::string drone_id;


// };

// struct DroneStatus_ {
//     std::string drone_id;


// };

class DockingStatus{
    public:
        DockingStatus() {
            tags = "";
            failed_frames = 0;
            successful_frames = 0;
            docking_attempts = 0;
            prev_iter_detection = false;
            has_centered = false;
        }

        mavsdk::geometry::CoordinateTransformation* ct;
        PIDController pid;
        std::string tags;
        cv::Mat img;

        int failed_frames;
        int successful_frames;
        int docking_attempts;

        bool prev_iter_detection;
        bool has_centered;
};

enum DockingIterationResult{
    DOCKING_SUCCESS,
    DOCKING_FAILURE,
    ITERATION_SUCCESS,
    RESTART_DOCKING
};

#endif
