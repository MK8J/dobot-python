import sys
import os
sys.path.append( os.path.dirname(os.path.dirname(__file__)))

from time import sleep

from lib.interface import Interface


def connect():
    '''
    A function to connect to the dobot.
    This is called by the other examples so you 
    dont have to change them all to connect to your dobot
    '''
    # windows
    bot = Interface('COM4')
    # for mac
    #bot = Interface('/dev/tty.SLAB_USBtoUART')

    print('Bot status:', 'connected' if bot.connected else 'not connected')

    return bot

if __name__=='__main__':
    bot = connect()
    # disconnecting
    bot.serial.close()
    

