import traceback as Etraceback

import apis.basic.const as Bconst
import apis.basic.error as Berror
import apis.frame.log as Flog

logName = "Frame-Error"


def Error(errorDescription=None):
    # 记录版本。
    Flog.WriteLog(logName, "Version now: " + Bconst.GetValue("programVersion") + ".", 0)
    # 记录开发者给出的错误信息。
    if errorDescription == None or type(errorDescription) != str:
        Flog.WriteLog(logName, "There isn't any returned information.", 0)
    else:
        Flog.WriteLog(logName, "Returned information: " + errorDescription, 0)
    # 记录Python的错误信息。
    tracebackInfo = Etraceback.format_exc()
    if tracebackInfo == "NoneType: None\n":
        Flog.WriteLog(logName, "There isn't any python built-in trace back.", 0)
    else:
        Flog.WriteLog(logName, "Python built-in trace back:\n\n" + tracebackInfo, 0)
    Berror.Error(errorDescription)
