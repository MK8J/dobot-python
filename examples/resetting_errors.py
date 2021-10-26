'''
A script to try and reset from a stage error
without having to turn off the dobot
'''
import sys
import os
sys.path.append(os.path.abspath('..'))

import connecting
#connect
bot = connecting.connect()

bot.reset_pose(1,45,45) # 0 is false, will try to automatically reset?
bot.clear_alarms_state() 
bot.serial.close()



#import homing
