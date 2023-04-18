from pymavlink import mavutil

# Set the connection parameters (modify as needed)
connection_string = 'udp:127.0.0.1:14550'
baud_rate = 57600

# Create a MAVLink connection
mav = mavutil.mavlink_connection(connection_string, baud=baud_rate)

# Wait for the heartbeat message from the drone
mav.wait_heartbeat()

# Print some information about the drone
print("Connected to MAVLink device with system ID: %d, component ID: %d" % (mav.target_system, mav.target_component))
print("Vehicle mode: %s" % mav.mode_mapping()[mav.flightmode])
print("Armed state: %s" % mavutil.mavlink.enums['ARMED'][mav.motors_armed()])

# Send a message to the drone
msg = mavutil.mavlink.MAVLink_heartbeat_message(6, 8, 0, 0, 0)
mav.send(msg)
