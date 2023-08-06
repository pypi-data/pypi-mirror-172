from .predefinedcolors import *
from conkits.csi import Cursor
from conkits.conio import Conio
from conkits.printtools import LivePrint, Choice


C256 = Colors256
normal_lp = LivePrint()  # 普通
simply_described_lp = LivePrint(print_delay=0.015, step=10)  # 打印简短描述
tips_lp = LivePrint(step=2, csi_code=Style.ITALICs)  # 打印小提示
interactive_lp = LivePrint(print_delay=0.005, step=1)  # 交互式打印
simple_description_of_usage = ''
options = [
    ' 如何使用Fore, Back, Style ',
    ' 如何使用Colors256',
    ' 如何使用Conio',
    ' 如何使用LivePrint',
    f' 如何使用Choice',
    ' 返回主菜单'
]
triangle = f'{Style.BRIGHTs + Fore.CYANs}▶{Style.NORMALs}'
current_index = f'  {triangle} {Fore.WHITEs + Style.DIMs}help{Style.NORMALs} {triangle} {Fore.GREENs + Style.BRIGHTs}usage{Fore.RESETs}'


def usage_of_conkits():
    usage_choice = Choice(options=options)
    while True:
        print()
        normal_lp.lprint(Style.BRIGHTs + current_index + Style.NORMALs, step=2)
        idx = usage_choice.run()
        if idx == len(options) - 1:
            break