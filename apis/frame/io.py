import apis.basic.clear as Bclear
import apis.frame.check as Fcheck
import apis.frame.error as Ferror
import apis.frame.lang as Flang
import apis.frame.log as Flog

logName = "Frame-Io"


# 输出文本。
def PrintText(outputLocation, outputString, outputVariable=None):  # 输出位置；提示字符串；提示字符串变量。
    outputLocation = Flang.FinalLang("apis.frame.output.output_location", [Flang.FinalLang(outputLocation)])  # 输出位置。
    outputString = Flang.ParseString(Flang.FindLang(outputString), outputVariable)  # 输出字符串。
    finalString = outputLocation + outputString  # 合并字符串。
    print(finalString)  # 输出，


# 输出自定义文本。
def PrintCustomText(outputString, outputVariable=None):
    finalString = Flang.ParseString(Flang.FindLang(outputString), outputVariable)  # 输出字符串。
    print(finalString)  # 输出。


# 输出空行。
def PrintEmptyLine():
    print()  # 输出。


# 输入值。
def InputValue(inputLocation, inputRequirement, inputString, inputVariable=None, isAgain=0):
    # 输入位置，输入需求，输入提示字符串，输入提示字符串变量，是否为重来。
    # 如果是重来，则更新输入提示。
    inputPrompt = ""
    if isAgain == 0:
        inputPrompt = ""
    elif isAgain == 700:
        Ferror.Error("Too many incorrect inputs.")
    else:
        inputPrompt = Flang.FinalLang("apis.frame.input.wrong_input")
    afterInputLocation = Flang.FinalLang("apis.frame.input.input_location", [Flang.FinalLang(inputLocation)])  # 输入位置。
    afterInputString = Flang.FinalLang(inputString, inputVariable)  # 输入提示字符串。
    finalString = afterInputLocation + inputPrompt + afterInputString  # 最终提示用户字符串。
    returnValue = input(finalString)  # 输入。
    # 如果输入不合法，则再次输入。
    if not Fcheck.DataCheck(returnValue, inputRequirement):
        returnValue = InputValue(inputLocation, inputRequirement, inputString, inputVariable, isAgain + 1)
    return returnValue


# 清除屏幕。
def ClearScreen():
    Flog.WriteLog(logName, "Screen cleared.", 3)  # 输出日志。
    Bclear.ClearScreen()  # 清除屏幕。
