import os as Eos

import apis.frame.io as Fio
import apis.frame.exit as Fexit
import apis.frame.log as Flog

logName = "Functions-System-Restart"
displayName = "functions.system.restart.name"


# 开始函数。
def Start():
    # 清除屏幕。
    Fio.ClearScreen()
    # 重新运行。
    Eos.system("start python.exe main.py")
    # 写入日志。
    Flog.WriteLog(logName, "Successfully restart the program.", 3)
    # 退出程序。
    Fexit.Exit()
