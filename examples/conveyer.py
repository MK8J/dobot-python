
import sys
import os
sys.path.append(os.path.abspath('..'))
import time

import connecting
import struct
#connect

class Message:
    def __init__(self, b=None):
        if b is None:
            self.header = bytes([0xAA, 0xAA])
            self.len = 0x00
            self.ctrl = 0x00
            self.params = bytes([])
            self.checksum = None
        else:
            self.header = b[0:2]
            self.len = b[2]
            self.id = b[3]
            self.ctrl = b[4]
            self.params = b[5:-1]
            self.checksum = b[-1:][0]

    def refresh(self):
        if self.checksum is None:
            self.checksum = self.id + self.ctrl
            for i in range(len(self.params)):
                if isinstance(self.params[i], int):
                    self.checksum += self.params[i]
                else:
                    self.checksum += int(self.params[i].encode('hex'), 16)
            self.checksum = self.checksum % 256
            self.checksum = 2 ** 8 - self.checksum
            self.checksum = self.checksum % 256
            self.len = 0x02 + len(self.params)

    def bytes(self):
        self.refresh()
        if len(self.params) > 0:
            command = bytearray([0xAA, 0xAA, self.len, self.id, self.ctrl])
            command.extend(self.params)
            command.append(self.checksum)
        else:
            command = bytes([0xAA, 0xAA, self.len, self.id, self.ctrl, self.checksum])
        return command


bot = connecting.connect()
print('')
index= 0

print('turn the motor on a slow speed')
# turn the motor on a slow speed
bot.set_extended_motor_velocity(index=index,enable=True, speed =1000)

time.sleep(2)
print('turn the motor on a fast speed')
bot.set_extended_motor_velocity(index=index,enable=True, speed= 10000)


time.sleep(2)
print('turn the motor on a fast speed the other way')
bot.set_extended_motor_velocity(index=index,enable=True, speed=0)
bot.set_extended_motor_velocity(index=index,enable=True, speed=-10000)
time.sleep(2)


bot.set_extended_motor_velocity(index=index,enable=False, speed=10000)
bot.serial.close()
