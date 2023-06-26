import os as Eos
import apis.basic.const as Bconst
import apis.frame.io as Fio
import apis.frame.log as Flog


displayName = "functions.system.clear.name"
logName = "Functions-System-Clear"


# 开始函数。
def Start():
    # 清除屏幕。
    Fio.ClearScreen()
    # 输出已清除屏幕提示。
    Fio.PrintText(displayName, "main.output.welcome_line_1")
    Fio.PrintText(displayName, "main.output.welcome_line_2", [Bconst.GetValue("programVersion")])
    Fio.PrintText(displayName, "functions.system.clear.output.finish")
    # 输出日志。
    Flog.WriteLog(logName, "Successfully clear the screen.", 3)
