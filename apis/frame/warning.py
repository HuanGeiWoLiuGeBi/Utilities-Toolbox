import os as Eos
import time

import apis.frame.config as Fconfig
import apis.frame.io as Fio
import apis.frame.log as Flog

logName = "Frame-Warning"
displayName = "apis.frame.warning.name"

warningList = []


def ProcessingPrompt(promptString, timeLevel=0):
    # 清除屏幕。
    Eos.system("cls")
    # 打印信息。
    print(promptString)
    if timeLevel == 0:
        print("Please be patient, it won't take long.")
    elif timeLevel == 1:
        print("Please be patient, the time spent depends on the network speed.")
    elif timeLevel == 2:
        print("Please be patient, this usually takes a long time.")
    else:
        print(str(timeLevel))


def PrintWarning():
    # 如果没有警告信息，则返回。
    if len(warningList) == 0:
        return
    # 如果设置了不打印警告，则返回。
    if Fconfig.GetConfigValue("config/global.scfg", "print_warning") == "False":
        return
    Flog.WriteLog(logName, "Start: print warnings.", 3)
    # 清除屏幕。
    Eos.system("cls")
    # 插入第一条警示信息。
    warningList.insert(0, ["apis.frame.warning.first_warning"])
    # 逐个输出警告信息。
    for singleWarning in warningList:
        if len(singleWarning) == 1:
            singleWarning.append([])
        Fio.PrintText(displayName, singleWarning[0], singleWarning[1])
        Fio.InputValue(displayName, None, "apis.frame.warning.confirm")
        Eos.system("cls")
    Flog.WriteLog(logName, "End: print warnings.", 3)
