import serial
import threading

from .message import Message


class Interface:
    def __init__(self, port):
        threading.Thread.__init__(self)
        self.lock = threading.Lock()

        self.serial = serial.Serial(
            port=port,
            baudrate=115200,
            parity=serial.PARITY_NONE,
            stopbits=serial.STOPBITS_ONE,
            bytesize=serial.EIGHTBITS, 
            timeout=2,
        )

    def send(self, message):
        self.lock.acquire()
        self.serial.write(message.package())
        self.serial.flush()
        response = Message.read(self.serial)
        self.lock.release()
    
        if response is None:
            return None

        return response.params

    @property
    def connected(self):
        '''
        returns if the serial port is open, not if it is connected to the dobot
        '''
        return self.serial.isOpen()

    def get_device_serial_number(self):
        request = Message([0xAA, 0xAA], 2, 0, False, False, [], direction='out')
        return self.send(request)

    def set_device_serial_number(self, serial_number):
        request = Message([0xAA, 0xAA], 2, 0, True, False, [serial_number], direction='out')
        return self.send(request)

    def get_device_name(self):
        request = Message([0xAA, 0xAA], 2, 1, False, False, [], direction='out')
        return self.send(request)

    def set_device_name(self, device_name):
        request = Message([0xAA, 0xAA], 2, 1, True, False, [device_name], direction='out')
        return self.send(request)

    def get_device_version(self):
        request = Message([0xAA, 0xAA], 2, 2, False, False, [], direction='out')
        return self.send(request)

    def set_sliding_rail_status(self, enable, version):
        request = Message([0xAA, 0xAA], 2, 3, True, False, [], direction='out')
        return self.send(request)

    # Time in milliseconds since start
    def get_device_time(self):
        request = Message([0xAA, 0xAA], 2, 4, False, False, [], direction='out')
        return self.send(request)

    def get_device_id(self):
        request = Message([0xAA, 0xAA], 2, 5, False, False, [], direction='out')
        return self.send(request)

    def get_pose(self):
        request = Message([0xAA, 0xAA], 2, 10, False, False, [], direction='out')
        return self.send(request)

    def reset_pose(self, manual, rear_arm_angle=None, front_arm_angle=None):
        '''

        Parameters
        ----------
        manual: int
            can be either 0 or 1. (sudo bool). 
            0 is if you don't need to provide an angle measurement, 1 is you do
        rear_arm_angle: float (optional)
            if manual = 1, you need to provide the angle of the "rear arm"
        front_arm_angle: float (optional)
            if manual = 1, you need to provide the angle of the "front arm"

        '''
        if manual == 1:
            assert rear_arm_angle is not None
            assert front_arm_angle is not None
        else:
            rear_arm_angle=0
            front_arm_angle=0
        request = Message([0xAA, 0xAA], 2, 11, True, False, [manual, rear_arm_angle, front_arm_angle], direction='out')
        return self.send(request)

    def get_sliding_rail_pose(self):
        request = Message([0xAA, 0xAA], 2, 13, False, False, [], direction='out')
        return self.send(request)

    def get_alarms_state(self):
        request = Message([0xAA, 0xAA], 2, 20, False, False, [], direction='out')
        return self.send(request)

    def clear_alarms_state(self):
        request = Message([0xAA, 0xAA], 2, 21, True, False, [], direction='out')
        return self.send(request)

    def get_homing_paramaters(self):
        request = Message([0xAA, 0xAA], 2, 30, False, False, [], direction='out')
        return self.send(request)

    def set_homing_parameters(self, x, y, z, r, queue=True):
        request = Message([0xAA, 0xAA], 2, 30, True, queue, [x, y, z, r], direction='out')
        return self.send(request)

    def set_homing_command(self, command, queue=True):
        request = Message([0xAA, 0xAA], 2, 31, True, queue, [command], direction='out')
        return self.send(request)

    # TODO: Reference is wrong here, arm does not send the said value
    def get_auto_leveling(self):
        request = Message([0xAA, 0xAA], 2, 32, False, False, [], direction='out')
        return self.send(request)

    def set_auto_leveling(self, enable, accuracy, queue=True):
        request = Message([0xAA, 0xAA], 2, 32, True, queue, [enable, accuracy], direction='out')
        return self.send(request)

    def get_handheld_teaching_mode(self):
        request = Message([0xAA, 0xAA], 2, 40, False, False, [], direction='out')
        return self.send(request)

    def set_handheld_teaching_mode(self, mode):
        request = Message([0xAA, 0xAA], 2, 40, True, False, [mode], direction='out')
        return self.send(request)

    def get_handheld_teaching_state(self):
        request = Message([0xAA, 0xAA], 2, 41, False, False, [], direction='out')
        return self.send(request)

    def set_handheld_teaching_state(self, enable):
        request = Message([0xAA, 0xAA], 2, 41, True, False, [enable], direction='out')
        return self.send(request)

    def get_handheld_teaching_trigger(self):
        request = Message([0xAA, 0xAA], 2, 42, False, False, [], direction='out')
        return self.send(request)

    def get_end_effector_params(self):
        request = Message([0xAA, 0xAA], 2, 60, False, False, [], direction='out')
        return self.send(request)

    def set_end_effector_params(self, bias_x, bias_y, bias_z):
        request = Message([0xAA, 0xAA], 2, 60, True, False, [bias_x, bias_y, bias_z], direction='out')
        return self.send(request)

    def get_end_effector_laser(self):
        request = Message([0xAA, 0xAA], 2, 61, False, False, [], direction='out')
        return self.send(request)

    def set_end_effector_laser(self, enable_control, enable_laser, queue=True):
        request = Message([0xAA, 0xAA], 2, 61, True, queue, [enable_control, enable_laser], direction='out')
        return self.send(request)

    def get_end_effector_suction_cup(self):
        request = Message([0xAA, 0xAA], 2, 62, False, False, [], direction='out')
        return self.send(request)

    def set_end_effector_suction_cup(self, enable_control, enable_suction, queue=True):
        request = Message([0xAA, 0xAA], 2, 62, True, queue, [enable_control, enable_suction], direction='out')
        return self.send(request)

    def get_end_effector_gripper(self):
        request = Message([0xAA, 0xAA], 2, 63, False, False, [], direction='out')
        return self.send(request)

    def set_end_effector_gripper(self, enable_control, enable_grip, queue=True):
        request = Message([0xAA, 0xAA], 2, 63, True, queue, [enable_control, enable_grip], direction='out')
        return self.send(request)

    def get_jog_joint_params(self):
        request = Message([0xAA, 0xAA], 2, 70, False, False, [], direction='out')
        return self.send(request)

    # TODO: Does not work - but is implemented according to spec. Bad documentation?
    def set_jog_joint_params(self, velocity, acceleration, queue=True):
        request = Message([0xAA, 0xAA], 2, 70, True, queue, velocity + acceleration, direction='out')
        return self.send(request)

    def get_jog_coordinate_params(self):
        request = Message([0xAA, 0xAA], 2, 71, False, False, [], direction='out')
        return self.send(request)

    # TODO: Does not work - but is implemented according to spec. Bad documentation?
    def set_jog_coordinate_params(self, velocity, acceleration, queue=True):
        request = Message([0xAA, 0xAA], 2, 71, True, queue, velocity + acceleration, direction='out')
        return self.send(request)

    def get_jog_common_params(self):
        request = Message([0xAA, 0xAA], 2, 72, False, False, [], direction='out')
        return self.send(request)

    # TODO: Does not work - but is implemented according to spec. Bad documentation?
    def set_jog_common_params(self, velocity_ratio, acceleration_ratio, queue=True):
        request = Message([0xAA, 0xAA], 2, 72, True, queue, [velocity_ratio, acceleration_ratio], direction='out')
        return self.send(request)

    def set_jog_command(self, jog_type, command, queue=True):
        '''
        
        performs a jog command.

        Parameters
        ----------
        jog_type : int
            can be 0 or 1. 0 is coordinate jog, 1 is joint jog
        command : int
            can be 0-8. This is the coordinate or joint to move.
            zero can be used to stop the jog
           
            value   coordinate  joint
            0       null        null
            1       X+          Joint1+
            2       X-          Joint1-
            3       Y+          Joint2+
            4       Y-          Joint2-
            5       Z+          Joint3+
            6       Z-          Joint3-
            7       R+          Joint4+
            8       R-          Joint4-

        queue : bool
            If a queue is to be used.

        '''
        request = Message([0xAA, 0xAA], 2, 73, True, queue, [jog_type, command], direction='out')
        return self.send(request)

    def get_sliding_rail_jog_params(self):
        request = Message([0xAA, 0xAA], 2, 74, False, False, [], direction='out')
        return self.send(request)

    def set_sliding_rail_jog_params(self, velocity, acceleration, queue=True):
        request = Message([0xAA, 0xAA], 2, 74, True, queue, [velocity, acceleration], direction='out')
        return self.send(request)

    def get_point_to_point_joint_params(self):
        request = Message([0xAA, 0xAA], 2, 80, False, False, [], direction='out')
        return self.send(request)

    def set_point_to_point_joint_params(self, velocity, acceleration, queue=True):
        request = Message([0xAA, 0xAA], 2, 80, True, queue, velocity + acceleration, direction='out')
        return self.send(request)

    def get_point_to_point_coordinate_params(self):
        request = Message([0xAA, 0xAA], 2, 81, False, False, [], direction='out')
        return self.send(request)

    def set_point_to_point_coordinate_params(self, coordinate_velocity, effector_velocity, coordinate_acceleration, effector_acceleration, queue=True):
        request = Message([0xAA, 0xAA], 2, 81, True, queue, [coordinate_velocity, effector_velocity, coordinate_acceleration, effector_acceleration], direction='out')
        return self.send(request)

    def get_point_to_point_jump_params(self):
        request = Message([0xAA, 0xAA], 2, 82, False, False, [], direction='out')
        return self.send(request)

    def set_point_to_point_jump_params(self, jump_height, z_limit, queue=True):
        request = Message([0xAA, 0xAA], 2, 82, True, queue, [jump_height, z_limit], direction='out')
        return self.send(request)

    def get_point_to_point_common_params(self):
        request = Message([0xAA, 0xAA], 2, 83, False, False, [], direction='out')
        return self.send(request)

    def set_point_to_point_common_params(self, velocity_ratio, acceleration_ratio, queue=True):
        request = Message([0xAA, 0xAA], 2, 83, True, queue, [velocity_ratio, acceleration_ratio], direction='out')
        return self.send(request)

    def set_point_to_point_command(self, mode, x, y, z, r, queue=True):
        '''
        moves to dobot arm from one point to another.
        Taken from Dobot Communication Protocol V1.0.4
       
        Parameters
        ----------

        mode: int
            How to move
                int     meaning          coordinates
                0       jump             xyz
                1       joint movement   xyz
                2       linear movement  xyz
                3       jump             ijk - angles of the robot arms
                4       joint movement   ijk
                5       linear movement  ijk
                6       joint movment    increment angle
                7       linear increment increment angle
                8       joint increment  joint increment, XYZ
                9       jump and linear  XYZ
        x: float
            the x dimension or i angle
        y: float
            the y dimension or angle j
        z: float
            the z dimension or the k angle
        r: float
            the rotation of the hand -- if applicable ?
            
        '''

        request = Message([0xAA, 0xAA], 2, 84, True, queue, [mode, x, y, z, r], direction='out')
        return self.send(request)

    def get_point_to_point_sliding_rail_params(self):
        request = Message([0xAA, 0xAA], 2, 85, False, False, [], direction='out')
        return self.send(request)

    def set_point_to_point_sliding_rail_params(self, velocity, acceleration, queue=True):
        request = Message([0xAA, 0xAA], 2, 85, True, queue, [velocity, acceleration], direction='out')
        return self.send(request)

    def set_point_to_point_sliding_rail_command(self, mode, x, y, z, r, l, queue=True):
        request = Message([0xAA, 0xAA], 2, 86, True, queue, [mode, x, y, z, r, l], direction='out')
        return self.send(request)

    def get_point_to_point_jump2_params(self):
        request = Message([0xAA, 0xAA], 2, 87, False, False, [], direction='out')
        return self.send(request)

    def set_point_to_point_jump2_params(self, start_height, end_height, z_limit, queue=True):
        request = Message([0xAA, 0xAA], 2, 87, True, queue, [start_height, end_height, z_limit], direction='out')
        return self.send(request)

    # TODO: Reference is ambigious here - needs testing
    def set_point_to_point_po_command(self, mode, x, y, z, r, queue=True):
        request = Message([0xAA, 0xAA], 2, 88, True, queue, [mode, x, y, z, r], direction='out')
        return self.send(request)

    # TODO: Reference is ambigious here - needs testing
    def set_point_to_point_sliding_rail_po_command(self, ratio, address, level, queue=True):
        request = Message([0xAA, 0xAA], 2, 89, True, queue, [ratio, address, level], direction='out')
        return self.send(request)

    def get_continous_trajectory_params(self):
        request = Message([0xAA, 0xAA], 2, 90, False, False, [], direction='out')
        return self.send(request)

    def set_continous_trajectory_params(self, max_planned_acceleration, max_junction_velocity, acceleration, queue=True):
        request = Message([0xAA, 0xAA], 2, 90, True, queue, [max_planned_acceleration, max_junction_velocity, acceleration, 0], direction='out')
        return self.send(request)

    def set_continous_trajectory_real_time_params(self, max_planned_acceleration, max_junction_velocity, period, queue=True):
        request = Message([0xAA, 0xAA], 2, 90, True, queue, [max_planned_acceleration, max_junction_velocity, period, 1], direction='out')
        return self.send(request)

    def set_continous_trajectory_command(self, mode, x, y, z, velocity, queue=True):
        request = Message([0xAA, 0xAA], 2, 91, True, queue, [mode, x, y, z, velocity], direction='out')
        return self.send(request)

    def set_continous_trajectory_laser_engraver_command(self, mode, x, y, z, power, queue=True):
        request = Message([0xAA, 0xAA], 2, 92, True, queue, [mode, x, y, z, power], direction='out')
        return self.send(request)

    def get_arc_params(self):
        request = Message([0xAA, 0xAA], 2, 100, False, False, [], direction='out')
        return self.send(request)

    def set_arc_params(self, coordinate_velocity, effector_velocity, coordinate_acceleration, effector_acceleration, queue=True):
        request = Message([0xAA, 0xAA], 2, 100, True, queue, [coordinate_velocity, effector_velocity, coordinate_acceleration, effector_acceleration], direction='out')
        return self.send(request)

    def set_arc_command(self, circumference_point, ending_point, queue=True):
        request = Message([0xAA, 0xAA], 2, 101, True, queue, circumference_point + ending_point, direction='out')
        return self.send(request)

    def wait(self, milliseconds, queue=True):
        request = Message([0xAA, 0xAA], 2, 110, True, queue, [milliseconds], direction='out')
        return self.send(request)

    def set_trigger_command(self, address, mode, condition, threshold, queue=True):
        request = Message([0xAA, 0xAA], 2, 120, True, queue, [address, mode, condition, threshold], direction='out')
        return self.send(request)

    def get_io_multiplexing(self):
        request = Message([0xAA, 0xAA], 2, 130, False, False, [], direction='out')
        return self.send(request)

    def set_io_multiplexing(self, address, multiplex, queue=True):
        '''
        sets multiplexing - really seems to be the extended items I/O type?

        Parameters
        ----------
        address: 8bit int
            An EIO address. (Extensible I/O adrdress)
        multiplex: int
            A IOMultiplexing type
                value   meaning
                0       Not in use
                1       PWM Output
                2       Digital Output
                3       Digital Input
                4       Analgue input

            These appear in a different order in Dobit API V1.0.0
            to Dobot Communication Protocol V1.0.4
        '''
        request = Message([0xAA, 0xAA], 2, 130, True, queue, [address, multiplex], direction='out')
        return self.send(request)

    def get_io_do(self):
        request = Message([0xAA, 0xAA], 2, 131, False, False, [], direction='out')
        return self.send(request)

    def set_io_do(self, address, level, queue=True):
        '''
        sets an extensible I/O  to either high or low

        Parameters
        ----------
        address: 8bit int
            An EIO address. (Extensible I/O adrdress)
        level: int
            can be 0 or 1. (low or high)
        '''
        request = Message([0xAA, 0xAA], 2, 131, True, queue, [address, level], direction='out')
        return self.send(request)

    def get_io_pwm(self):
        request = Message([0xAA, 0xAA], 2, 132, False, False, [], direction='out')
        return self.send(request)

    def set_io_pwm(self, address, frequency, duty_cycle, queue=True):
        '''
        sets PWM to the extended I/O  
        from to Dobot Communication Protocol V1.0.4

        Parameters
        ----------
        address: 8bit int
            An EIO address. (Extensible I/O adrdress)
        frequency: float
            the PWM frequency 10 - 10e6, in units of Hz
        duty_cycle: float
            is says 0-100. 
        '''
        request = Message([0xAA, 0xAA], 2, 132, True, queue, [address, frequency, duty_cycle], direction='out')
        return self.send(request)

    def get_io_di(self):
        request = Message([0xAA, 0xAA], 2, 133, False, False, [], direction='out')
        return self.send(request)

    def get_io_adc(self):
        '''
        reads an analogue value?
        from to Dobot Communication Protocol V1.0.4
        '''
        request = Message([0xAA, 0xAA], 2, 134, False, False, [], direction='out')
        return self.send(request)

    def set_extended_motor_velocity(self, index, enable, speed, queue=True):
        '''
        sets the motot velocity of an extended motor

        Parameters
        ----------
        index : index
            can be either 0 or 1. 0 is stepper motor 1? and 1 is stepper motor 2?
        enable : bool
            Is motor control enabled
        speed : int
            The speed of the motor in pulses per second
        '''
        request = Message([0xAA, 0xAA], 2, 135, 1, queue, [index, enable, int(speed)], direction='out')
        return self.send(request)

    def get_color_sensor(self, index):
        request = Message([0xAA, 0xAA], 2, 137, False, False, [], direction='out')
        return self.send(request)

    def set_color_sensor(self, index, enable, port, version, queue=True):
        request = Message([0xAA, 0xAA], 2, 137, True, queue, [enable, port, version], direction='out')
        return self.send(request)

    def get_ir_switch(self, index):
        request = Message([0xAA, 0xAA], 2, 138, False, False, [], direction='out')
        return self.send(request)

    def set_ir_switch(self, index, enable, port, version, queue=True):
        request = Message([0xAA, 0xAA], 2, 138, True, queue, [enable, port, version], direction='out')
        return self.send(request)

    def get_angle_sensor_static_error(self, index):
        request = Message([0xAA, 0xAA], 2, 140, False, False, [], direction='out')
        return self.send(request)

    def set_angle_sensor_static_error(self, index, rear_arm_angle_error, front_arm_angle_error):
        request = Message([0xAA, 0xAA], 2, 140, True, False, [rear_arm_angle_error, front_arm_angle_error], direction='out')
        return self.send(request)

    def get_wifi_status(self):
        request = Message([0xAA, 0xAA], 2, 150, False, False, [], direction='out')
        return self.send(request)

    def set_wifi_status(self, index, enable):
        request = Message([0xAA, 0xAA], 2, 150, True, False, [enable], direction='out')
        return self.send(request)

    def get_wifi_ssid(self):
        request = Message([0xAA, 0xAA], 2, 151, False, False, [], direction='out')
        return self.send(request)

    def set_wifi_ssid(self, index, ssid):
        request = Message([0xAA, 0xAA], 2, 151, True, False, [ssid], direction='out')
        return self.send(request)

    def get_wifi_password(self):
        request = Message([0xAA, 0xAA], 2, 152, False, False, [], direction='out')
        return self.send(request)

    def set_wifi_password(self, index, ssid):
        request = Message([0xAA, 0xAA], 2, 152, True, False, [ssid], direction='out')
        return self.send(request)

    def get_wifi_address(self):
        request = Message([0xAA, 0xAA], 2, 153, False, False, [], direction='out')
        return self.send(request)

    # 192.168.1.1 = a.b.c.d
    def set_wifi_address(self, index, use_dhcp, a, b, c, d):
        request = Message([0xAA, 0xAA], 2, 153, True, False, [use_dhcp, a, b, c, d], direction='out')
        return self.send(request)

    def get_wifi_netmask(self):
        request = Message([0xAA, 0xAA], 2, 154, False, False, [], direction='out')
        return self.send(request)

    # 255.255.255.0 = a.b.c.d
    def set_wifi_netmask(self, index, a, b, c, d):
        request = Message([0xAA, 0xAA], 2, 154, True, False, [a, b, c, d], direction='out')
        return self.send(request)

    def get_wifi_gateway(self):
        request = Message([0xAA, 0xAA], 2, 155, False, False, [], direction='out')
        return self.send(request)

    # 192.168.1.1 = a.b.c.d
    def set_wifi_gateway(self, index, use_dhcp, a, b, c, d):
        request = Message([0xAA, 0xAA], 2, 155, True, False, [use_dhcp, a, b, c, d], direction='out')
        return self.send(request)

    def get_wifi_dns(self):
        request = Message([0xAA, 0xAA], 2, 156, False, False, [], direction='out')
        return self.send(request)

    # 192.168.1.1 = a.b.c.d
    def set_wifi_dns(self, index, use_dhcp, a, b, c, d):
        request = Message([0xAA, 0xAA], 2, 156, True, False, [use_dhcp, a, b, c, d], direction='out')
        return self.send(request)

    def get_wifi_connect_status(self):
        request = Message([0xAA, 0xAA], 2, 157, False, False, [], direction='out')
        return self.send(request)

    def set_lost_step_params(self, param):
        request = Message([0xAA, 0xAA], 2, 170, True, False, [param], direction='out')
        return self.send(request)

    def set_lost_step_command(self):
        request = Message([0xAA, 0xAA], 2, 171, True, False, [], direction='out')
        return self.send(request)

    def start_queue(self):
        request = Message([0xAA, 0xAA], 2, 240, True, False, [], direction='out')
        return self.send(request)

    def stop_queue(self, force=False):
        request = Message([0xAA, 0xAA], 2, 242 if force else 241, True, False, [], direction='out')
        return self.send(request)

    def start_queue_download(self, total_loop, line_per_loop):
        request = Message([0xAA, 0xAA], 2, 243, True, False, [total_loop, line_per_loop], direction='out')
        return self.send(request)

    def stop_queue_download(self):
        request = Message([0xAA, 0xAA], 2, 244, True, False, [], direction='out')
        return self.send(request)

    def clear_queue(self):
        request = Message([0xAA, 0xAA], 2, 245, True, False, [], direction='out')
        return self.send(request)

    def get_current_queue_index(self):
        request = Message([0xAA, 0xAA], 2, 246, True, False, [], direction='out')
        return self.send(request)
