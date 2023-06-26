import os as Eos
import time as Etime

import apis.frame.config as Fconfig
import apis.frame.exit as Fexit
import apis.frame.log as Flog
import apis.frame.io as Fio

displayName = "functions.system.exit.name"
logName = "Functions-System-Exit"


# 开始函数。
def Start():
    # 清除屏幕。
    Fio.ClearScreen()
    # 获取退出等待时间。
    exitWaitTime = Fconfig.GetConfigValue("config/system/global.scfg", "exit_wait_time")
    # 输出信息。
    Fio.PrintText(displayName, "functions.system.exit.output.finish_1")
    Fio.PrintText(displayName, "functions.system.exit.output.finish_2", [exitWaitTime])
    # 等待时间。
    Etime.sleep(int(exitWaitTime))
    # 输出成功日志。
    Flog.WriteLog(logName, "Successfully exit the program.", 3)
    # 退出程序。
    Fexit.Exit()
