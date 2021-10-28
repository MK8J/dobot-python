import sys
import os
import time
print(__file__)
sys.path.append(os.path.abspath('..'))

from time import sleep

from lib.interface import Interface

import connecting
#connect
bot = connecting.connect()

joint_params = bot.get_point_to_point_joint_params()
print('Joint params:', joint_params)

jump_params = bot.get_point_to_point_jump_params()
print('Jump params:', jump_params)

jump2_params = bot.get_point_to_point_jump2_params()
print('Jump2 params:', jump2_params)

common_params = bot.get_point_to_point_common_params()
print('Common params:', common_params)

coordinate_params = bot.get_point_to_point_coordinate_params()
print('Coordinate params:', coordinate_params)

# Does nothing?
#bot.set_point_to_point_command(0, 10, 10, 10, 10)
#sleep(1)

# Does nothing?
#bot.set_point_to_point_command(1, 30, 30, 30, 30)
#sleep(1)
# One axis at a time
pose = bot.get_pose()
x,y,z,r = pose[:4]
for i in range(1):
    z += 0.50
    bot.set_point_to_point_command(2, x, y, z, r)
    time.sleep(0.01)
1/0
# One axis at a time
bot.set_point_to_point_command(3, 30, 30, 30, 30)
sleep(1)

# Shortest path
bot.set_point_to_point_command(4, 10, 10, 10, 10)
sleep(1)

# Shortest path
bot.set_point_to_point_command(5, 30, 30, 30, 30)
sleep(1)

# Shortest path
bot.set_point_to_point_command(6, 10, 10, 10, 10)
sleep(1)

# Shortest path
bot.set_point_to_point_command(7, 30, 30, 30, 30)
sleep(1)

bot.set_point_to_point_command(8, 10, 10, 10, 10)
sleep(1)

# Does nothing?
bot.set_point_to_point_po_command(0, 30, 30, 30, 30)
