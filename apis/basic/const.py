# 定义基础值。
def GetValue(variableName):
    varibleDict = {
        "programVersion": "ALPHA-0.1.3",  # 程序字符串版本。
        "programVersionCode": 13,  # 程序数字版本。
        "nowInformationFormatVersion": 1  # 程序支持组格式版本。
    }
    return varibleDict.get(variableName, "[UNDEFINED]")
