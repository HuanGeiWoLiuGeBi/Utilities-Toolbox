import os as Eos

import apis.basic.const as Bconst
import apis.frame.config as Fconfig
import apis.frame.error as Ferror
import apis.frame.io as Fio
import apis.frame.lang as Flang
import apis.frame.log as Flog
import apis.frame.register as Fregister
import apis.frame.runtime as Fruntime
import apis.frame.warning as Fwarning

logName = "Main"
displayName = "main.name"


# 加载框架
def LoadFrame():
    try:
        Fwarning.ProcessingPrompt("Stage: load frame.")
        # 初始化日志文件。
        Fwarning.ProcessingPrompt("Initializing the log file.")
        Flog.InitLog()
        # 记录运行环境。
        Fwarning.ProcessingPrompt("Initializing environment information.")
        Fruntime.InitEnvironmentInfo()
        # 初始化系统配置。
        Fwarning.ProcessingPrompt("Initializing system config files.")
        Fconfig.InitSystemConfig()
        # 初始化系统语言文件。
        Fwarning.ProcessingPrompt("Initializing system language files.")
        Flang.InitSystemLang()
        # 删除旧日志。
        Fwarning.ProcessingPrompt("Deleting old log files.")
        Flog.DeleteOldLog()
    except:
        Ferror.Error("Unable to load framework, please check your runtime environment.")


# 加载功能。
def LoadFunctions():
    try:
        Fwarning.ProcessingPrompt("Stage: load functions.")
        # 加载功能。
        Fregister.RegisterFunction()
        # 输出警告。
        Fwarning.PrintWarning()
    except:
        Ferror.Error("Unable to load functions, unknown error.")


# 加载程序。
def LoadProgram():
    try:
        # 运行一个功能。
        def RunFunction(functionName):
            for singleFunction in functionList:
                if singleFunction[0] == functionName:
                    singleFunction[1]()
                    break

        # 清除屏幕。
        Eos.system("cls")
        # 记录日志。
        Flog.WriteLog(logName, "Preload phase ended, start to ask user to run functions.", 3)
        # 输出欢迎语。
        Fio.PrintText(displayName, "main.output.welcome_line_1")
        Fio.PrintText(displayName, "main.output.welcome_line_2", [Bconst.GetValue("programVersion")])
        # 开始询问用户。
        functionList = Fregister.GetAllFunction()  # 函数触发名与函数地址。
        validInputValue = Fregister.GetAllFunctionName()  # 函数地址，用于判断输入是否合法。
        while True:
            # 输入。
            userInput = Fio.InputValue(displayName, validInputValue, "main.input.input_function_name")
            # 输出空行与运行。
            Flog.WriteLog(logName, "Start: run function - " + userInput + ".", 3)
            Fio.PrintEmptyLine()
            RunFunction(userInput)
            Fio.PrintEmptyLine()
            Flog.WriteLog(logName, "End: run function - " + userInput + ".", 3)
    except:
        Ferror.Error("Unable to run function, unknown error.")


# 主函数，程序执行的起点。
def Main():
    # 加载框架。
    LoadFrame()
    # 加载功能。
    LoadFunctions()
    # 加载程序。
    LoadProgram()


# 如果名称正常（非外部调用），则运行。
if __name__ == "__main__":
    # 执行程序。
    Main()
