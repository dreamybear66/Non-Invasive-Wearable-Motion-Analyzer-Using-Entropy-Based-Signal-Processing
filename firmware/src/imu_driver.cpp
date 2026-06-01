#include "imu_driver.h"
#include <Wire.h>
#include <MPU6050.h>

MPU6050 mpu;
float accelOffset[3] = {0,0,0};
float gyroOffset[3] = {0,0,0};

void IMU_Init() {
    Wire.begin();
    mpu.initialize();
    
    // Check connection
    if(!mpu.testConnection()){
        Serial.println("MPU6050 connection failed");
        while(1);
    }
    
    // Configure range: accel +/-8g, gyro +/-500 deg/s
    mpu.setFullScaleAccelRange(MPU6050_ACCEL_FS_8);
    mpu.setFullScaleGyroRange(MPU6050_GYRO_FS_500);
    
    IMU_Calibrate();
}

void IMU_Calibrate() {
    Serial.println("Calibrating IMU... Keep device still.");
    long sum_ax = 0, sum_ay = 0, sum_az = 0;
    long sum_gx = 0, sum_gy = 0, sum_gz = 0;
    int samples = 200;
    
    for(int i = 0; i < samples; i++) {
        int16_t ax, ay, az, gx, gy, gz;
        mpu.getMotion6(&ax, &ay, &az, &gx, &gy, &gz);
        sum_ax += ax; sum_ay += ay; sum_az += az;
        sum_gx += gx; sum_gy += gy; sum_gz += gz;
        delay(5);
    }
    
    accelOffset[0] = (sum_ax / samples) / 4096.0; // 8g scale
    accelOffset[1] = (sum_ay / samples) / 4096.0;
    accelOffset[2] = ((sum_az / samples) / 4096.0) - 1.0; // Gravity on Z
    
    gyroOffset[0] = (sum_gx / samples) / 65.5; // 500 deg/s scale
    gyroOffset[1] = (sum_gy / samples) / 65.5;
    gyroOffset[2] = (sum_gz / samples) / 65.5;
}

IMUData readIMU() {
    int16_t ax, ay, az, gx, gy, gz;
    mpu.getMotion6(&ax, &ay, &az, &gx, &gy, &gz);
    
    IMUData data;
    data.ax = (ax / 4096.0) - accelOffset[0];
    data.ay = (ay / 4096.0) - accelOffset[1];
    data.az = (az / 4096.0) - accelOffset[2];
    
    data.gx = (gx / 65.5) - gyroOffset[0];
    data.gy = (gy / 65.5) - gyroOffset[1];
    data.gz = (gz / 65.5) - gyroOffset[2];
    
    return data;
}
