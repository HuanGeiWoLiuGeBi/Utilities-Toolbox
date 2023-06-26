import re as Ere
import types as Etypes

import apis.frame.error as Ferror

logName = "Frame-Check"


# 检查数据。
def DataCheck(dataCheck, requirementString):  # 要检查的数据；数据的正则表达式。
    # 如果要检查的数据类型不是字符串，则直接返回不合格。
    if not type(dataCheck) == str:
        return False
    # 如果要求是字符串，那么即为正则表达式。
    if type(requirementString) == str:
        try:
            returnValue = Ere.match(requirementString, dataCheck).group()
            if returnValue == dataCheck:
                return True
            else:
                return False
        except:
            return False
    # 如果要求是列表，那么即为列表内值。
    elif type(requirementString) == list:
        if dataCheck in requirementString:
            return True
        else:
            return False
    # 如果是自定义函数，则让函数判断。
    elif type(requirementString) == Etypes.FunctionType:
        return requirementString(dataCheck)
    # 如果是无，则无条件。
    elif requirementString is None:
        return True
    # 都不是则报错。
    else:
        Ferror.Error("Regular expression or check list format error. From: " + requirementString + ".")


# 判断单个字符串是否仅由某些字符组成。
def StringCheck(stringCheck, whiteList):
    for singleChar in stringCheck:
        if singleChar not in whiteList:
            return False
    return True
