#!/usr/bin/env python3
# -*- encoding: utf-8 -*-

#######################################
# #!/usr/bin/env python3
# # -*- encoding: utf-8 -*-
# # 将py文件编译成pyc 二进制文件
# import py_compile
# py_compile.compile("jumplogin.py")
#######################################

import pexpect
import os
import sys
import struct
import fcntl
import termios
import signal


jumpIP="192.168.88.20"
jumpPort="22"
jumpUser="www"
jumpPasswd="123456"

user_infos={
     "test": {"addr": "192.168.88.101", "port": "22", "username": "www", "passwd": "123456"},
    "proxy": {"addr": "192.168.88.101", "port": "22", "username": "www", "passwd": "123456"},
     "prod": {"addr": "192.168.88.101", "port": "22", "username": "www", "passwd": "123456"}
}


# 获取窗口大小
def getwinsize():
    """This returns the window size of the child tty.
    The return value is a tuple of (rows, cols).
    """
    if 'TIOCGWINSZ' in dir(termios):
        TIOCGWINSZ = termios.TIOCGWINSZ
    else:
        TIOCGWINSZ = "1074295912L"
    s = struct.pack('HHHH', 0, 0, 0, 0)
    x = fcntl.ioctl(sys.stdout.fileno(), TIOCGWINSZ, s)
    return struct.unpack('HHHH', x)[0:2]


def login_jumpserver(curent_user):
    #发送命令执行交互
    user_info = user_infos.get(curent_user)
    child = pexpect.spawn('/usr/bin/ssh  -p {} {}@{}'.format(jumpPort,jumpUser,jumpIP))

    # 重新获取窗口大小
    def sigwinch_passthrough (sig, data):
        winsize = getwinsize()
        child.setwinsize(winsize[0],winsize[1])
        # print("行: ",winsize[0],"列:",winsize[1])

    # 窗口大小改变时触发信号
    signal.signal(signal.SIGWINCH, sigwinch_passthrough)

    sz = os.get_terminal_size()
    child.setwinsize(sz.lines,sz.columns)
    # print("行: ",sz.lines,"列:",sz.columns)

    child.expect ('password:')
    child.sendline('{}'.format(jumpPasswd))

    child.expect('vmtom')
    child.sendline('/usr/bin/ssh  -p {} {}@{}'.format(user_info.get("port"),user_info.get("username"),user_info.get("addr")))
    child.expect('password:')
    child.sendline('{}'.format(user_info.get("passwd")))
    child.interact()

def main():
    menuShow = """
        1.  登入test跳板机
        2.  登入proxy跳板机
        3.  登入prod跳板机
        q.  退出
        
    """
    print(menuShow)
    while True:
        try:
            select = input("请选择功能选项：")
            if select == 1 or select == "1":
                login_jumpserver("test")
                break
            elif select == 2 or select == "2":
                login_jumpserver("proxy")
                break
            elif select == 3 or select == "3":
                login_jumpserver("prod")
                break
            elif select in ["q","quit","exit"]:
                exit(0)
        except Exception as ex:
            print("异常退出")
            exit(0)

if __name__ == "__main__":
    main()

