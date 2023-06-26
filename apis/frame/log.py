import datetime as Edatetime
import os as Eos
import time as Etime

import apis.frame.config as Fconfig
import apis.frame.file as Ffile

logName = "Frame-Log"

currentLogFileName = "None"  # 目前的日志文件路径及名称。
currentLogFileCreateTime = "None"  # 目前日志文件创建的时间。
logLevelDict = {
    0: "FATAL",  # 必须终止程序的错误。
    1: "ERROR",  # 局部出现错误，需要知晓，但无需终止程序。
    2: "WARN",  # 出现可以解决的错误。
    3: "INFO",  # 用于记录重要事件。
    4: "DEBUG"  # 用于开发者记录程序运行中的变量。
}  # 等级对应的提示。


# 创建新的日志文件。
def NewLogFile(filePath):
    # 如果路径已被占用，那么返回没有创建成功。
    if Ffile.IsSomethingExists(filePath):
        return False
    # 创建一个新的。
    Ffile.NewFile(filePath)
    # 返回创建成功。
    return True


# 初始化日志文件。
def InitLog():
    global currentLogFileName
    global currentLogFileCreateTime
    # 记录当前时间。
    currentLogFileCreateTime = Etime.strftime("%Y-%m-%d_%H-%M-%S", Etime.localtime())
    # 创建日志文件。
    currentTryNum = 1
    while True:
        currentLogFileName = "logs/" + currentLogFileCreateTime + "_" + str(currentTryNum) + ".log"
        createResult = NewLogFile(currentLogFileName)  # 创建结果。
        # 创建成功则跳出循环，否则继续尝试。
        if createResult == True:
            break
        currentTryNum = currentTryNum + 1
    WriteLog(logName, "Successfully initialize log file.", 3)


# 写入日志。
def WriteLog(logFileName, logContent, logLevel):  # 函数显示名称；日志内容；日志级别。
    # 如果日志还没创建，那么不记录。
    if currentLogFileName == "None":
        return
    # 判断日志级别并赋值给对应提示。
    logLevelName = logLevelDict.get(logLevel, "UNKNOW")
    # 检查日志文件，若没有，则新建一个日志文件。
    if not Ffile.IsFileExists(currentLogFileName):
        # 创建日志文件。
        Ffile.DeleteSomething(currentLogFileName)
        Ffile.NewFile(currentLogFileName)
        # 给出警告。
        WriteLog(logName, "Can't found the log file, create a new one.", 2)
    # 记录日志内容。
    logTime = Edatetime.datetime.now().strftime("%Y_%m_%d-%H:%M:%S-%f")
    writeContent = "[" + logLevelName + "] [" + logTime + "] [" + logFileName + "] " + logContent + "\n"
    Ffile.AddFileContent(currentLogFileName, writeContent)


# 删除旧日志。
def DeleteOldLog():
    # 如果用户配置要删除，则删除，否则不删除。
    if Fconfig.GetConfigValue("config/global.scfg", "delete_old_log") == "True":
        WriteLog(logName, "Start: delete old log files.", 3)
        # 创建所有的日志文件名称列表。
        logFileList = Eos.listdir("logs/")
        # 删除列表中的文件。
        for chooseFileName in logFileList:
            # 如果是目前的文件，不删除。
            if "logs/" + chooseFileName != currentLogFileName:
                Ffile.DeleteSomething("logs/" + chooseFileName)
        WriteLog(logName, "End: delete old log files.", 3)
