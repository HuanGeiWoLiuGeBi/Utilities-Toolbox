import apis.frame.check as Fcheck
import apis.frame.error as Ferror
import apis.frame.file as Ffile
import apis.frame.log as Flog

logName = "Frame-Config"

configList = []  # 配置列表


def SplitLine(singleLine):
    backupLine = singleLine
    lineLen = len(backupLine)  # 字符串的长度。
    charNow = 0  # 当前读取的字符。
    configID = ""  # 配置名字。
    configDescription = ""  # 配置描述。
    configContent = ""  # 配置内容。
    # 分出来配置名字。
    while True:
        # 如果到末尾，就不合法。
        if charNow == lineLen:
            return False
        # 如果是等于，则进入下一板块。
        if backupLine[charNow] == "=":
            charNow = charNow + 1
            break
        configID = configID + backupLine[charNow]
        charNow = charNow + 1
    # 若ID为空，则不合法。
    if configID == "":
        return False
    # 分出来配置描述。
    while True:
        # 如果到末尾，就不合法。
        if charNow == lineLen:
            return False
        # 如果是等于，则进入下一板块。
        if backupLine[charNow] == "=":
            charNow = charNow + 1
            break
        configDescription = configDescription + backupLine[charNow]
        charNow = charNow + 1
    # 若描述为空，则不合法。
    if configDescription == "":
        return False
    # 分出来配置内容。
    while True:
        # 如果是末尾或最后一个字符是\，跳出循环。
        if charNow == lineLen - 1 and backupLine[charNow] == "\\":
            break
        if charNow == lineLen - 1:
            return False
        configContent = configContent + backupLine[charNow]
        charNow = charNow + 1
    # 返回。
    return [configID, configDescription, configContent]


# 检查一项配置。
def CheckConfig(filePath, optionList):
    # 检查某字符串是否含有等于。
    def CheckString(checkString):
        for singleChar in checkString:
            if singleChar == "=":
                return False
        return True

    optionNameList = []
    # 检查每一个选项是否符合格式要求。
    for singleOption in optionList:
        # 如果单个选项格式不对，则报错。
        if type(singleOption) != list or len(singleOption) != 4:
            Ferror.Error("Option format error: " + singleOption[0] + ".")
        # 分离。
        optionName = singleOption[0]
        optionDescription = singleOption[1]
        optionDefaultValue = singleOption[2]
        requirementString = singleOption[3]
        # 如果名称和介绍含等号，则报错。
        if not (CheckString(optionName) and CheckString(optionDescription)):
            Ferror.Error("Option name or description value setting error: " + singleOption[0] + ".")
        # 如果名称第一个字是注释符，则报错。
        if optionName[0] == "#":
            Ferror.Error("Option name value setting error: " + singleOption[0] + ".")
        # 如果默认值不符合需求值，则报错。
        if not Fcheck.DataCheck(optionDefaultValue, requirementString):
            Ferror.Error("Option default value setting error: " + singleOption[0] + ".")
        # 如果选项已经存在过，则报错。
        if optionName in optionList:
            Ferror.Error("Duplicate register option: " + singleOption[0] + ".")
        optionNameList.append(optionName)
    # 如果文件不存在或不可读，则删除。
    if (not Ffile.IsFileExists(filePath)) or (not Ffile.CanRead(filePath)):
        Ffile.DeleteSomething(filePath)
        Ffile.NewFile(filePath)
        Flog.WriteLog(logName, "Read file failed: " + filePath + ", create a new one.", 2)
    fileContent = Ffile.ReadFile(filePath)  # 文件内容。
    splitByLine = fileContent.split("\n")  # 使用换行符切割。
    lineNum = len(splitByLine)  # 总行数。
    isRead = []  # 所有已读选项。
    # 分析每行内容。
    for lineNow in range(0, lineNum):
        # 如果是空行，则跳过。
        if splitByLine[lineNow] == "":
            continue
        # 如果是注释行，则跳过。
        if splitByLine[lineNow][0] == "#":
            continue
        # 分割，如果不合法，则注释掉，下一个。
        lineInfo = SplitLine(splitByLine[lineNow])
        if lineInfo == False:
            splitByLine[lineNow] = "#" + splitByLine[lineNow]
            continue
        # 分离。
        optionName = lineInfo[0]
        optionValue = lineInfo[2]
        # 如果已经有过这个值，注释掉。
        if optionName in isRead:
            splitByLine[lineNow] = "#" + splitByLine[lineNow]
            continue
        for singleOption in optionList:
            # 如果分离出来的名字是选项的名字。
            if singleOption[0] == optionName:
                afterName = optionName  # 重置名称。
                afterDescription = singleOption[1]  # 重置描述。
                # 重置值。
                if Fcheck.DataCheck(optionValue, singleOption[3]):
                    configList.append([filePath, optionName, optionValue])
                    afterValue = optionValue
                else:
                    Flog.WriteLog(logName, "Option value setting error: " + optionName + ".", 2)
                    configList.append([filePath, optionName, singleOption[2]])
                    afterValue = singleOption[2]
                afterLine = afterName + "=" + afterDescription + "=" + afterValue + "\\"
                splitByLine[lineNow] = afterLine
                isRead.append(optionName)
                break

    # 最后一行是空行则删除。
    if splitByLine[-1] == "":
        splitByLine.pop()
    # 如果没有读到值，则添加一行并记录默认值。
    for singleOption in optionList:
        # 如果没有读到。
        if not singleOption[0] in isRead:
            Flog.WriteLog(logName, "Find option failed: " + singleOption[0] + ", create a new one.", 2)
            configList.append([filePath, singleOption[0], singleOption[2]])
            splitByLine.append(singleOption[0] + "=" + singleOption[1] + "=" + singleOption[2] + "\\")
    fileContent = ""
    # 还原文件并写入。
    for singleLine in splitByLine:
        fileContent = fileContent + singleLine + "\n"
    Ffile.ChangeFile(filePath, fileContent)


# 加载配置。
def InitSystemConfig():
    Flog.WriteLog(logName, "Start: load system configurations.", 3)
    CheckConfig("config/global.scfg", [
        ["delete_old_log", "none", "True", "(True|False)"],
        ["language", "none", "en_us", "[a-z,A-Z,_]{1,50}"],
        ["print_warning", "none", "True", "(True|False)"],
        ["pip_install_server", "none", "https://pypi.org/simple/", None]
    ])
    Flog.WriteLog(logName, "End: load system configurations.", 3)


# 获取配置值。
def GetConfigValue(filePath, optionName):
    returnValue = None
    for configOption in configList:
        if configOption[0] == filePath and configOption[1] == optionName:
            returnValue = configOption[2]
            break
    if returnValue == None:
        Ferror.Error("Can't find configuration: " + filePath + " - " + optionName + ".")
    return returnValue
