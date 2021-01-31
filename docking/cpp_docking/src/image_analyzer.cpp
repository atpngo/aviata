#include "image_analyzer.hpp"
#include "util.hpp"

#include <opencv2/core.hpp>
#include <opencv2/core/types.hpp>
#include <opencv2/imgcodecs.hpp>
#include <opencv2/highgui.hpp>
#include <opencv2/imgproc.hpp>

#include "apriltag.h"
#include "tag36h11.h"

#include <string>
#include <math.h>
#include <vector>
#include <algorithm>

ImageAnalyzer::ImageAnalyzer(){
    tf=tagStandard36h11_create();
    m_tagDetector=apriltag_detector_create();
    apriltag_detector_add_family(m_tagDetector,tf);

}
ImageAnalyzer::~ImageAnalyzer(){
    apriltag_detector_destroy(m_tagDetector);
    tagStandard36h11_destroy(tf);
}

float* ImageAnalyzer::processImage(Mat img, int ind, float yaw, std::string& tags){
    float* errs=new float[4];

    int width=img.cols;
    int height=img.rows;
    Point2f image_center(img.cols / 2, img.rows / 2);

    Mat rot_mat = getRotationMatrix2D(image_center, -1.0*yaw, 1.0);
    warpAffine(img, img, rot_mat, Size(img.cols, img.rows), INTER_LINEAR, BORDER_CONSTANT, Scalar(255, 255, 255));
    cvtColor(img,img,COLOR_BGR2GRAY);

    zarray_t dets=m_tagDetector->extractTags(img);

    std::string tagsDetected="";
    for(int i=0;i<zarray_size(dets);i++){
        apriltag_detection_t *det;
        zarray_get(dets,i,&det);
        if(det->decision_margin>=MARGIN){
            tagsDetected+=det->id+" ";
        }
    }
    tags=tagsDetected;

    for(int i=0;i<zarray_size(dets);i++){
        apriltag_detection_t *det;
        zarray_get(dets,i,&det);
        if(det->id==ind&&det->decision_margin>=MARGIN){
            double* center=det->c;
            double rect[4][2]=det->p;

            std::vector<float> sideList;
            for(int i=0;i<4;i++){
                for(int j=i+1;j<4;j++){
                    sideList.push_back((float)sqrt(pow((rect[i][0]-rect[j][0]),2)+pow((rect[i][1]-rect[j][1]),2)));
                }
            }
            std::sort(sideList.begin(),sideList.end());
            float sideAvg=0;
            for(int i=0;i<4;i++){
                sideAvg+=sideList[i];
            }
            sideAvg/=4.0;
            float tag_pixel_ratio;
            if(ind==0){
                tag_pixel_ratio=((float)CENTRAL_TAG_SIZE)/sideAvg;
            }
            else{
                tag_pixel_ratio=((float)PERIPHERAL_TAG_SIZE)/sideAvg;
            }

            errs[2]=0.50/tan((CAMERA_FOV_HORIZONTAL*0.50)*M_PI/180.0)*width*tag_pixel_ratio;

            float y3=rect[3].second;
            float y0=rect[0].second;
            float x3=rect[3].first;
            float x0=rect[0].first;

            float incline_angle;
            if(x3-x0!=0){
                incline_angle=180.0/M_PI *atan2(y3-y0,x3-x0);
                incline_angle=incline_angle*-1.0+90.0;
                if(incline_angle>0){
                    incline_angle-=180;
                }
                else{
                    incline_angle+=180;
                }
            }
            else if(y3>y0){
                incline_angle=-180;
            }
            else{
                incline_angle=0;
            }
            errs[3]=incline_angle*-1;

            float x_offset=center.first-image_center.x;
            float y_offset=center.second-image_center.y;
            errs[0]=x_offset*tag_pixel_ratio;
            errs[1]=y_offset*tag_pixel_ratio;
            return errs;
        }
        log("Image Analyzer: ","Desired apriltag not found, aborting",true);
        return nullptr;
    }
    return nullptrt;
}