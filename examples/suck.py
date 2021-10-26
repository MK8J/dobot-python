
import os
import sys
from time import sleep
sys.path.append('..')
from lib import Interface

bot = Interface('COM4')

print('Bot status:', 'connected' if bot.connected else 'not connected')

#status = bot.get_end_effector_suction_cup()
#print('Status:', status)
print('contol enabled')
bot.set_end_effector_suction_cup(enable_control=True, enable_suction=False)
sleep(2)

print('suction on')
bot.set_end_effector_suction_cup(enable_control=True, enable_suction=True)
sleep(2)

print('suction off')
bot.set_end_effector_suction_cup(enable_control=True, enable_suction=False)
sleep(2)

print('suction disabled')
bot.set_end_effector_suction_cup(enable_control=False, enable_suction=False)

bot.serial.close()
print('Bot status:', 'connected' if bot.connected else 'not connected')
