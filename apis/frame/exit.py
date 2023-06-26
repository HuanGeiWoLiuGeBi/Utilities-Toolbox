import apis.basic.exit as Bexit
import apis.frame.log as Flog

logName = "Frame-Exit"


# 退出程序。
def Exit():
    # 记录日志。
    Flog.WriteLog(logName, "Successfully exit the program.", 3)
    # 退出程序。
    Bexit.Exit()
