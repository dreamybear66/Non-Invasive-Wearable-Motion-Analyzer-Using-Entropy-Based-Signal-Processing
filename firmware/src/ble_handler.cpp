#include "ble_handler.h"
#include <NimBLEDevice.h>

#define SERVICE_UUID        "1801" // Generic Attribute Profile (Customized for IMU)
#define CHARACTERISTIC_UUID "2A53" // Placeholder characteristic

NimBLEServer* pServer = NULL;
NimBLECharacteristic* pCharacteristic = NULL;
bool deviceConnected = false;

class MyServerCallbacks: public NimBLEServerCallbacks {
    void onConnect(NimBLEServer* pServer) {
      deviceConnected = true;
      Serial.println("Client connected");
    };

    void onDisconnect(NimBLEServer* pServer) {
      deviceConnected = false;
      Serial.println("Client disconnected");
      // Restart advertising
      NimBLEDevice::startAdvertising();
    }
};

void BLE_Init(const char* deviceName) {
    NimBLEDevice::init(deviceName);
    
    pServer = NimBLEDevice::createServer();
    pServer->setCallbacks(new MyServerCallbacks());
    
    NimBLEService *pService = pServer->createService(SERVICE_UUID);
    pCharacteristic = pService->createCharacteristic(
                        CHARACTERISTIC_UUID,
                        NIMBLE_PROPERTY::NOTIFY
                      );
                      
    pService->start();
    
    NimBLEAdvertising *pAdvertising = NimBLEDevice::getAdvertising();
    pAdvertising->addServiceUUID(SERVICE_UUID);
    pAdvertising->setScanResponse(true);
    pAdvertising->start();
    
    Serial.println("BLE Advertising started");
}

bool BLE_IsConnected() {
    return deviceConnected;
}

void BLE_SendPacket(uint32_t packet_id, float ax, float ay, float az, float gx, float gy, float gz, uint8_t battery) {
    if (!deviceConnected) return;
    
    // Packet structure: <I f f f f f f B
    uint8_t buffer[29];
    memcpy(buffer, &packet_id, 4);
    memcpy(buffer + 4, &ax, 4);
    memcpy(buffer + 8, &ay, 4);
    memcpy(buffer + 12, &az, 4);
    memcpy(buffer + 16, &gx, 4);
    memcpy(buffer + 20, &gy, 4);
    memcpy(buffer + 24, &gz, 4);
    buffer[28] = battery;
    
    pCharacteristic->setValue(buffer, 29);
    pCharacteristic->notify();
}
