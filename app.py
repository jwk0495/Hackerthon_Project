# -*- coding: utf-8 -*-

import collections
import collections.abc
collections.MutableMapping = collections.abc.MutableMapping

from flask import Flask, render_template
from flask_socketio import SocketIO, emit
from dronekit import connect, VehicleMode, LocationGlobalRelative
import time
import threading

# --- Flask, SocketIO 초기화 ---
app = Flask(__name__, template_folder='templates', static_folder='static')
app.config['SECRET_KEY'] = 'drone_web_controller_secret'
socketio = SocketIO(app)

# --- DroneKit 차량 객체 ---
vehicle = None

# --- DroneKit 연결 시도 ---
# MAVProxy 등을 통해 UDP로 스트리밍되는 MAVLink에 연결합니다.
connection_string = 'udp:127.0.0.1:14550'
try:
    print(f"Connecting to vehicle on: {connection_string}")
    vehicle = connect(connection_string, wait_ready=True, timeout=60)
    print("Vehicle Connected!")
except Exception as e:
    print(f"Error connecting to vehicle: {e}")
    print("Running in simulation mode without vehicle connection.")


# --- 주기적으로 드론 상태를 UI로 전송하는 스레드 ---
def drone_status_updater():
    """index2.html의 'drone_status_update' 이벤트를 처리합니다."""
    while True:
        if vehicle:
            status = {
                'position': {
                    'x': vehicle.location.global_relative_frame.lat,  # UI의 x를 위도로 가정
                    'y': vehicle.location.global_relative_frame.alt,  # UI의 y를 고도로 가정
                    'z': vehicle.location.global_relative_frame.lon   # UI의 z를 경도로 가정
                },
                'altitude': vehicle.location.global_relative_frame.alt,
                'battery': vehicle.battery.voltage,  # 필요시 %로 변환
                'mission_state': vehicle.mode.name,
                'payload_type': 'N/A'  # 페이로드는 별도 관리 필요
            }
            socketio.emit('drone_status_update', status)
        time.sleep(1)  # 1초 간격


# --- UI의 명령을 받아 DroneKit으로 실행하는 핸들러 ---

@socketio.on('arm_drone')
def handle_arm_drone():
    """UI의 '시동 (Arm)' 버튼에 대응"""
    if vehicle and not vehicle.armed:
        print("Command: Arming motors")
        vehicle.mode = VehicleMode("GUIDED")
        vehicle.armed = True
        emit('server_message', 'Drone Armed!')

@socketio.on('disarm_drone')
def handle_disarm_drone():
    """UI의 '시동 끄기 (Disarm)' 버튼에 대응"""
    if vehicle and vehicle.armed:
        print("Command: Disarming motors")
        vehicle.armed = False
        emit('server_message', 'Drone Disarmed!')

@socketio.on('takeoff')
def handle_takeoff(data):
    """UI의 '이륙' 버튼에 대응"""
    if vehicle and vehicle.armed:
        target_altitude = float(data.get('altitude', 5))
        print(f"Command: Takeoff to {target_altitude}m")
        vehicle.simple_takeoff(target_altitude)
        emit('server_message', f'Takeoff command sent to {target_altitude}m.')

@socketio.on('land_drone')
def handle_land_drone():
    """UI의 '착륙' 버튼에 대응"""
    if vehicle:
        print("Command: Landing")
        vehicle.mode = VehicleMode("LAND")
        emit('server_message', 'Landing command sent.')

@socketio.on('report_wildfire')
def handle_goto_location(data):
    """UI의 '목표 지점으로 이동' 버튼에 대응"""
    if vehicle:
        coords = data['coordinates']
        target_location = LocationGlobalRelative(coords['x'], coords['z'], float(coords['y']))
        print(f"Command: Fly to Lat:{coords['x']}, Lon:{coords['z']}, Alt:{coords['y']}")
        vehicle.mode = VehicleMode("GUIDED")
        vehicle.simple_goto(target_location)
        emit('server_message', f"Moving to target location.")

@socketio.on('force_return_pressed')
def handle_force_return():
    """UI의 '강제 귀환' 버튼에 대응"""
    if vehicle:
        print("Command: RTL")
        vehicle.mode = VehicleMode("RTL")
        emit('server_message', 'RTL Mode Activated!')

@socketio.on('emergency_stop_pressed')
def handle_emergency_stop():
    """UI의 '즉시 착륙 (LAND)' 버튼에 대응"""
    if vehicle:
        print("Command: Emergency LAND")
        vehicle.mode = VehicleMode("LAND")
        emit('server_message', 'Emergency Landing command sent!')


# --- 기본 Flask 라우트 및 서버 실행 ---
@app.route('/')
def index():
    # index2.html을 기본 페이지로 렌더링
    return render_template('index2.html')

@app.route('/v2')
def index_v2():
    return render_template('index2.html')


if __name__ == '__main__':
    # 드론 상태 업데이트 스레드 시작
    if vehicle:
        updater_thread = threading.Thread(target=drone_status_updater)
        updater_thread.daemon = True
        updater_thread.start()

    # 웹 서버 실행
    print("Flask-SocketIO server starting...")
    socketio.run(app, host='0.0.0.0', port=8282)
