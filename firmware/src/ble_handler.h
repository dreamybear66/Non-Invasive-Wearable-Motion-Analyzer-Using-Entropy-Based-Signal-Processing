#ifndef BLE_HANDLER_H
#define BLE_HANDLER_H

#include <Arduino.h>

void BLE_Init(const char* deviceName);
void BLE_SendPacket(uint32_t packet_id, float ax, float ay, float az, float gx, float gy, float gz, uint8_t battery);
bool BLE_IsConnected();

#endif
