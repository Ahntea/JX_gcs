from django.shortcuts import render
from pymavlink import mavutil
from .models import Drone
from django.views.decorators.csrf import csrf_exempt

def connect_to_drone(request):
    # Set the connection parameters
    connection_string = 'udp:127.0.0.1:14550'
    baud_rate = 57600
    
    # Connect to the drone
    mav = mavutil.mavlink_connection(connection_string, baud=baud_rate)
    
    # Create a new Drone object and save it to the database
    drone = Drone(status='Connected')
    drone.save()
    
    return render(request, 'mavlink/connected.html')

def send_message(request):
    # Get the Drone object from the database
    drone = Drone.objects.get(pk=1)
    
    # Send a message to the drone
    mav = mavutil.mavlink_connection('udp:127.0.0.1:14550')
    mav.mav.heartbeat_send(mavutil.mavlink.MAV_TYPE_GCS, mavutil.mavlink.MAV_AUTOPILOT_INVALID, 0, 0, 0)
    
    # Update the Drone object in the database
    drone.status = 'Message sent'
    drone.save()
    
    return render(request, 'mavlink/message_sent.html')

def receive_message(request):
    # Get the Drone object from the database
    drone = Drone.objects.get(pk=1)
    
    # Receive a message from the drone
    mav = mavutil.mavlink_connection('udp:127.0.0.1:14550')
    msg = mav.recv_match()
    
    if msg:
        drone.status = 'Message received'
        drone.save()
    
    return render(request, 'mavlink/message_received.html')

# Connect to the drone's telemetry link
connection = mavutil.mavlink_connection('/dev/ttyUSB0', baud=57600)

@csrf_exempt
def control(request):
    if request.method == 'POST':
        # Parse the desired position and velocity from the request data
        x = float(request.POST.get('x', 0))
        y = float(request.POST.get('y', 0))
        z = float(request.POST.get('z', 0))
        vx = float(request.POST.get('vx', 0))
        vy = float(request.POST.get('vy', 0))
        vz = float(request.POST.get('vz', 0))

        # Compute the desired attitude commands using a control loop
        # TODO: Implement a control loop that can track a desired trajectory or set of waypoints
        roll = 0.0  # desired roll angle in radians
        pitch = 0.0  # desired pitch angle in radians
        yaw = 0.0  # desired yaw angle in radians

        # Send the attitude commands to the drone
        msg = mavutil.mavlink.MAVLink_attitude_target_message(
            0,  # time_boot_ms
            1,  # target_system
            1,  # target_component
            mavutil.mavlink.MAV_FRAME_BODY_NED,  # frame
            0b11111111,  # type_mask
            roll,  # roll
            pitch,  # pitch
            yaw,  # yaw
            0.0,  # body roll rate
            0.0,  # body pitch rate
            0.0,  # body yaw rate
            0.0,  # thrust
        )
        connection.mav.send(msg)

        # Compute the desired velocity commands using a control loop
        # TODO: Implement a control loop that can regulate the drone's velocity
        vx_cmd = vx  # desired velocity in the x-axis (forward)
        vy_cmd = vy  # desired velocity in the y-axis (right)
        vz_cmd = vz  # desired velocity in the z-axis (up)

        # Send the velocity commands to the drone
        msg = mavutil.mavlink.MAVLink_set_position_target_local_ned_encode(
            0,  # time_boot_ms
            1,  # target_system
            1,  # target_component
            mavutil.mavlink.MAV_FRAME_LOCAL_NED,  # frame
            0b000011111100011        ,  # type_mask
            x,  # x
            y,  # y
            z,  # z
            vx_cmd,  # vx
            vy_cmd,  # vy
            vz_cmd,  # vz
            0.0,  # afx
            0.0,  # afy
            0.0,  # afz
            0.0,  # yaw
            0.0,  # yaw_rate
        )
        connection.mav.send(msg)

    return render(request, 'drone_control/control.html')

