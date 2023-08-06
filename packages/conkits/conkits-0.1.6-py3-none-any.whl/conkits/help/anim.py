from .predefinedcolors import *
from conkits.csi import Cursor
from conkits.conio import Conio
from conkits.printtools import LivePrint, Choice

escape_characters = ['Q', 'q']


def wait_anim(char, print_delay=0.012):
    if char in escape_characters or Conio.getch() in escape_characters:
        return True
    else:
        return False

def wait_anim0(char):
    Cursor.hide()
    string = "press to continue ..."
    csi_code = Colors256.FORE237
    ch = None
    while True:
        if ch:
            Conio.erase_line()
            Cursor.show()
            return ch in escape_characters
        prt_str = ' ' * 20 if csi_code == 237 else string
        print(csi_code + prt_str + Style.RESET_ALLs)
        delay = 2 if csi_code == 237 else 0.06
        ch = Conio.interruptible_sleep(delay)
        Cursor.up(1)
        if ch:
            Conio.erase_line()
            Cursor.show()
            return ch in escape_characters
        csi_code += 1
        if csi_code == 255:
            while int(csi_code) > 237:
                delay = 0.8 if csi_code == 255 else 0.05
                csi_code -= 1
                print(csi_code + prt_str + Style.RESET_ALLs)
                ch = Conio.interruptible_sleep(delay)
                Cursor.up(1)
                if ch:
                    Conio.erase_line()
                    Cursor.show()
                    return ch in escape_characters

