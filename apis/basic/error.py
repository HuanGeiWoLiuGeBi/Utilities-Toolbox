import time as Etime
import traceback as Etraceback

import apis.basic.clear as Bclear
import apis.basic.const as Bconst
import apis.basic.exit as Bexit


def Error(errorDescription=None):
    # 清除屏幕。
    Bclear.ClearScreen()
    # 输出发生错误。
    print("The program crashed.")
    # 输出版本。
    print("Version now: " + Bconst.GetValue("programVersion") + ".")
    # 输出开发者给出的错误信息。
    if errorDescription == None or type(errorDescription) != str:
        print("There isn't any returned information.")
    else:
        print("Returned information: " + errorDescription, 0)
    # 输出Python的错误信息。
    tracebackInfo = Etraceback.format_exc()
    if tracebackInfo == "NoneType: None\n":
        print("There isn't any python built-in trace back.")
    else:
        print("Python built-in trace back:\n\n" + tracebackInfo)
    # 输出30秒后关闭窗口并休眠30秒后退出。
    print("This window will close in 30 seconds.")
    Etime.sleep(30)
    Bexit.Exit()
