import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from lib import Interface

import connecting

#connect
bot = connecting.connect()

params = bot.get_homing_paramaters()
print('Params:', params)

print('Homing')
bot.set_homing_command(0)

# there is a queue commant that
# tells you want command it has started
# we append a wait to the end of this to 
# tell us when it has finished homing

bot.wait(0)
queue_index = bot.get_current_queue_index()
while bot.get_current_queue_index != queue_index:
    pass

bot.serial.close()
