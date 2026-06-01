#include <Arduino.h>
#include "imu_driver.h"
#include "ble_handler.h"

uint32_t packet_id = 0;
unsigned long last_transmit_time = 0;
const int transmit_interval = 10; // 100 Hz

void setup() {
    Serial.begin(115200);
    IMU_Init();
    BLE_Init("SportsEL_IMU");
}

void loop() {
    if (millis() - last_transmit_time >= transmit_interval) {
        last_transmit_time = millis();
        
        IMUData imu = readIMU();
        
        // Mock battery level 95%
        uint8_t battery = 95;
        
        BLE_SendPacket(packet_id, imu.ax, imu.ay, imu.az, imu.gx, imu.gy, imu.gz, battery);
        packet_id++;
    }
}
