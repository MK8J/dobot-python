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
print('done')
bot.serial.close()
