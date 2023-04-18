from pymavlink import mavutil

# create a connection to the drone
connection_string = 'udp:127.0.0.1:14550'
connection = mavutil.mavlink_connection(connection_string)

# listen for incoming messages and decode them
while True:
    msg = connection.recv_match()
    if msg is None:
        continue
    if msg.get_type() == 'ATTITUDE':
        # retrieve the attitude from the message
        roll = msg.roll
        pitch = msg.pitch
        yaw = msg.yaw
        # print the attitude to the console
        print(f'Roll: {roll}, Pitch: {pitch}, Yaw: {yaw}')
    if msg.get_type() == 'GPS_RAW_INT':
        # retrieve the GPS location from the message
        lat = msg.lat / 1e7
        lon = msg.lon / 1e7
        # print the GPS location to the console
        print(f'Latitude: {lat}, Longitude: {lon}')
    elif msg.get_type() == 'GLOBAL_POSITION_INT':
        # retrieve the altitude and ground speed from the message
        alt = msg.alt / 1e3
        ground_speed = msg.vx / 100
        # print the altitude and ground speed to the console
        print(f'Altitude: {alt}, Ground Speed: {ground_speed}')
    elif msg.get_type() == 'HEARTBEAT':
        # retrieve the system status and battery voltage from the message
        system_status = mavutil.system_status_str(msg.system_status)
        battery_voltage = msg.voltage_battery / 1000
        # print the system status and battery voltage to the console
        print(f'System Status: {system_status}, Battery Voltage: {battery_voltage}')

