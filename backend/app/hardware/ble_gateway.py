import asyncio
import struct
import httpx
from datetime import datetime, timezone
from bleak import BleakClient, BleakScanner

# Constants
IMU_SERVICE_UUID = "1801" # Default placeholder for testing
IMU_CHAR_UUID = "2A53"    # Default placeholder for testing

async def process_imu_packet(sender, data: bytearray, session_id: str, sensor_id: str, http_client: httpx.AsyncClient):
    """
    Decodes the 20-byte IMU packet and sends to ingestion API.
    Packet struct: <I f f f f f f B
    (packet_id, acc_x, acc_y, acc_z, gyro_x, gyro_y, gyro_z, battery)
    """
    if len(data) != 29: # Exact packing size depends on struct definition
        return

    try:
        unpacked = struct.unpack('<IffffffB', data)
        packet = {
            "packet_id": unpacked[0],
            "acc_x": unpacked[1],
            "acc_y": unpacked[2],
            "acc_z": unpacked[3],
            "gyro_x": unpacked[4],
            "gyro_y": unpacked[5],
            "gyro_z": unpacked[6],
            "battery_pct": unpacked[7]
        }
        
        batch = {
            "sensor_id": sensor_id,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "packets": [packet]
        }
        
        # Post to local API
        await http_client.post(f"http://localhost:8000/api/v1/sessions/{session_id}/raw-data", json=batch)
    except Exception as e:
        print(f"Error decoding packet: {e}")

async def run_ble_gateway(device_address: str, session_id: str, sensor_id: str):
    """Connect to ESP32 and stream data"""
    async with httpx.AsyncClient() as http_client:
        async with BleakClient(device_address) as client:
            print(f"Connected to {device_address}")
            
            # Wrapper to pass session info
            async def notify_callback(sender, data):
                await process_imu_packet(sender, data, session_id, sensor_id, http_client)
            
            await client.start_notify(IMU_CHAR_UUID, notify_callback)
            print("Streaming started. Press Ctrl+C to stop.")
            
            while True:
                await asyncio.sleep(1)
