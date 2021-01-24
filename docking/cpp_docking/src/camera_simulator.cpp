#include "camera_simulator.hpp"
#include "util.hpp"

#include <string>
#include <iostream>

#include <cmath>
#include <opencv2/core.hpp>
#include <opencv2/core/types.hpp>
#include <opencv2/imgcodecs.hpp>
#include <opencv2/highgui.hpp>
#include <opencv2/imgproc.hpp>

using namespace cv;

CameraSimulator::CameraSimulator(Target target) 
    : m_log_tag("Camera Sim"), m_target(target) 
{
    m_scale_constant = get_view_scale_constant(TARGET_SIZE);
    m_peripheral_scale_constant = get_view_scale_constant(PERIPHERAL_TARGET_SIZE);

    m_display_width = (int) (DISPLAY_SCALE * tan(to_radians(CAMERA_FOV_HORIZONTAL / 2.0)));
    m_display_height = (int) (DISPLAY_SCALE * tan(to_radians(CAMERA_FOV_VERTICAL / 2.0)));

    m_april_tag = imread("../res/3_stage_tags.png"); // this path is relative to the binary executable, NOT this file's location    
    if(m_april_tag.empty())
    {
        log(m_log_tag, "Failed to load image", true);
    }
}

void CameraSimulator::update_target_location(Target t) {
    m_target = t;
}

float CameraSimulator::get_view_scale_constant(float target_size) {
    return DISPLAY_SCALE * target_size / 2.0 / 100.0;
}

Mat CameraSimulator::update_current_image(float absLon, float absLat, float absAlt, float absYaw, int target_id) {

    // Converts from absolute to relative coordinates
    float target_lat = m_target.lat;
    float target_lon = m_target.lon;
    float target_alt = m_target.alt;
    float target_yaw = m_target.yaw;
    if (target_id != 0) { // Adjusts for offset peripheral targets
        int target_offset = (target_id <= 3) ? abs(target_id - 3) * 45 : (11 - target_id) * 45;
        target_lat += DRONE_RADIUS * sin(to_radians(target_offset - target_yaw));
        target_lon += DRONE_RADIUS * cos(to_radians(target_offset - target_yaw));
        target_yaw += -1 * 360 / 8 * (target_id - 1);
    }

    float relativeLat = absLat - target_lat;
    float relativeLon = absLon - target_lon;
    float relativeAlt = absAlt - target_alt;
    float relativeYaw = absYaw - target_yaw; // degrees from north clockwise

    if (relativeAlt <= 0) {
        log("Camera Sim", "Altitude too low", true);
        return imread("../res/BACKGROUND.jpg");
    }

    // Resizes Image given the altitude and precomputed scale factor (scale precomputed for efficiency)
    int scale = 0;
    Mat april_tag;
    if (target_id == 0) {
        scale = abs((int) (m_scale_constant / relativeAlt));
        resize(m_april_tag, april_tag, Size(scale, scale), 0, 0);
    } else {
        std::string tag_name = "../res/peripheral_tags/tag36_11_0000" + std::to_string(target_id) + ".png";
        Mat loaded_image = imread(tag_name); // Each image is 10x10,should be ok to load each iteration but could be preloaded
        scale = abs((int) (m_peripheral_scale_constant / relativeAlt));
        resize(loaded_image, april_tag, Size(scale, scale), 0, 0);
    }

    // Sets translation of AprilTag
    // Converts cartesian translation to polar coordinates
    double translationDist = sqrt(relativeLat * relativeLat + relativeLon * relativeLon);
    double translationAngle = atan2(relativeLat, relativeLon) + to_radians(absYaw);

    // Adjusts for relative rotation then converts to pixel offset
    double common_ops = m_scale_constant * translationDist / 2.0 / relativeAlt;
    double offsetx = cos(translationAngle) * common_ops;
    double offsety = sin(translationAngle) * common_ops;

    // Rotates AprilTag without clipping
    // NOTE: opencv treats positive as ccw, but mavsdk treats positive as cw (which is what we use)
    // however, since the drone is rotating and not the image, the image must rotate in the opposite direction (so ccw)
    rotate_image(april_tag, relativeYaw);

    // Puts AprilTags on white canvas background, clipping edges if necessary
    Mat background = imread("../res/BACKGROUND.jpg");
    resize(background, background, Size(m_display_width, m_display_height), 0, 0);
    // img = april_tag;

    int x = (int) (m_display_width * 0.50 - offsetx - scale / 2.0);
    int y = (int) (m_display_height * 0.50 + offsety - scale / 2.0);
    
    Rect roi; // region of interest
    roi.width = april_tag.cols;
    roi.x = 0;
    roi.height = april_tag.rows;
    roi.y = 0;
    if (y < 0) { // crop top
        roi.y = -y;
        roi.height = roi.height - roi.y;
        y = 0;
    }
    if (x < 0) { // crop left
        roi.x = -x;
        roi.width = roi.width - roi.x;
        x = 0;
    }
    if (roi.height + y > background.rows) { // crop bottom
        roi.height = background.rows - y;
    }
    if (roi.width + x > background.cols) { // crop right
        roi.width = background.cols - x;
    }

    Mat crop = april_tag(roi);

    if (x < background.cols && y < background.rows) {
        Mat roi2(background, Rect(x, y, crop.cols, crop.rows));
        crop.copyTo(roi2);
    }

    imshow("Test", background);
    waitKey(1);
    
    return background; // change to background later
}


void CameraSimulator::rotate_image(Mat& image, double angle) {
    // Modified from https://stackoverflow.com/questions/9041681/opencv-python-rotate-image-by-x-degrees-around-specific-point
    // image_center = tuple(np.array(image.shape[1::-1]) / 2);
    Point2f image_center(image.cols / 2, image.rows / 2);
    Mat rot_mat = getRotationMatrix2D(image_center, angle, 1.0);
    warpAffine(image, image, rot_mat, Size(image.cols, image.rows), INTER_LINEAR, BORDER_CONSTANT, Scalar(255, 255, 255));
}