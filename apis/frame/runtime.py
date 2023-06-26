import ctypes as Ectypes
import os as Eos
import platform as Eplatform
import subprocess as Esubprocess
import sys as Esys

import apis.basic.const as Bconst
import apis.frame.config as Fconfig
import apis.frame.error as Ferror
import apis.frame.exit as Fexit
import apis.frame.log as Flog
import apis.frame.warning as Fwarning
import main

logName = "Frame-Runtime"

platformName = ""  # 平台名称。
platformRelease = ""  # 平台大版本。
platformVersion = ""  # 平台详细版本。
pythonVersion = ""  # Python版本。
programVersion = ""  # 程序本体版本。


# 记录环境信息。
def InitEnvironmentInfo():
    Flog.WriteLog(logName, "Start: check the environment.", 3)
    global platformName
    global platformRelease
    global platformVersion
    global pythonVersion
    global programVersion
    platformInformation = Eplatform.uname()
    platformName = platformInformation.system
    platformRelease = platformInformation.release
    platformVersion = platformInformation.version
    pythonVersion = Esys.version
    programVersion = Bconst.GetValue("programVersion")
    Flog.WriteLog(logName, "Platform name: " + platformName + ".", 3)
    Flog.WriteLog(logName, "System release: " + platformRelease + ".", 3)
    Flog.WriteLog(logName, "System version: " + platformVersion + ".", 3)
    Flog.WriteLog(logName, "Python version: " + pythonVersion, 3)
    Flog.WriteLog(logName, "Program version: " + programVersion, 3)
    Flog.WriteLog(logName, "End: check the environment.", 3)
    if platformName != "Windows":
        Fwarning.warningList.append(["apis.frame.runtime.suggest_windows"])
    else:
        if platformRelease != "10":
            Fwarning.warningList.append(["apis.frame.runtime.suggest_windows_10"])


# 安装Pip包。
def InstallPip(packageName):
    Fwarning.ProcessingPrompt("Installing package: " + packageName + ".", 1)
    returnValue = Esubprocess.getstatusoutput(
        "pip install " + packageName + " -i " + Fconfig.GetConfigValue("config/global.scfg", "pip_install_server"))
    if returnValue[0] != 0:
        Ferror.Error("Failed to install package: " + packageName + ".")


# 获取管理员权限。
def GetAdmin():
    try:
        # 防止颜色输出失效并更改背景颜色。
        Eos.system("")
        # 若不是管理员，则索要权限。
        if not Ectypes.windll.shell32.IsUserAnAdmin():
            Ectypes.windll.shell32.ShellExecuteW(None, "runas", Esys.executable, main.__file__, None, 1)
            Fexit.Exit()
    except:
        # 若无法获取，则报告错误。
        Ferror.Error("Unable to obtain administrator privilege.")
