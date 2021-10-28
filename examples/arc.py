import sys
import os
sys.path.append( os.path.dirname(os.path.dirname(__file__)))

from time import sleep

from lib.interface import Interface

import connecting
#connect
bot = connecting.connect()

params = bot.get_arc_params()
print('Params:', params)

# Default start position
#bot.set_homing_command(0)
#sleep(4)

[x, y, z, r] = bot.get_pose()[0:4]
print([x,y,z,r])
# this doesn't work
bot.set_arc_command([x, y, z, r], [x - 50, y + 50, z, r])
#bot.set_arc_command([x + 50, y, z, r], [x - 50, y + 50, z, r])
