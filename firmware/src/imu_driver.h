#ifndef IMU_DRIVER_H
#define IMU_DRIVER_H

#include <Arduino.h>

struct IMUData {
    float ax, ay, az;
    float gx, gy, gz;
};

void IMU_Init();
IMUData readIMU();
void IMU_Calibrate();

#endif
