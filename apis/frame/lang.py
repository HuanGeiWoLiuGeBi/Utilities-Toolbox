import apis.frame.config as Fconfig
import apis.frame.error as Ferror
import apis.frame.file as Ffile
import apis.frame.log as Flog

logName = "Frame-Lang"

langDictOriginal = dict()  # 英语映射表。
langDictDefault = dict()  # 用户指定语言映射表。
currentLang = "None"  # 用户指定语言。
colorDict = {
    "1": "30",  # 黑。
    "2": "31",  # 红。
    "3": "32",  # 绿。
    "4": "33",  # 黄。
    "5": "34",  # 蓝。
    "6": "35",  # 紫。
    "7": "36",  # 青。
    "8": "37",  # 白。
}  # 颜色映射表。
backgroundDict = {
    "1": "40",  # 黑。
    "2": "41",  # 红。
    "3": "42",  # 绿。
    "4": "44",  # 黄。
    "5": "44",  # 蓝。
    "6": "45",  # 紫。
    "7": "46",  # 青。
    "8": "47",  # 白。
}  # 背景颜色映射表。
wayDict = {
    "1": "0",  # 默认。
    "2": "1",  # 高亮。
    "3": "4",  # 下划线。
    "4": "5",  # 闪烁。
}  # 显示方式映射表。


# 寻找并解析语言文件。
def FinalLang(langDescription, stringVariable=None):
    return ParseString(FindLang(langDescription), stringVariable)


# 寻找语言文件。
def FindLang(langDescription):
    # 如果英语没有，则报错，若有，则继续查找用户需要语言，有则返回，无责返回英语。
    defaltValue = ""
    try:
        defaltValue = langDictOriginal[langDescription]
    except:
        Ferror.Error("Can't find language string: " + langDescription + ".")
    try:
        needValue = langDictDefault[langDescription]
        return needValue
    except:
        return defaltValue


# 解析字符串。
def ParseString(originalString, stringVariable=None):  # 要解析的字符串；字符串里带的变量。
    if stringVariable is None:
        stringVariable = []
    if not type(stringVariable) == list:
        Ferror.Error("Variable format error. From: " + originalString + ".")
    returnValue = ""  # 设置返回值。
    useVariableCount = 0  # 已经用到的变量个数。
    notDoNext = 0  # 下一次不检查标记。
    for pointNumber in range(0, len(originalString)):  # 逐个遍历字符。
        # 若不检查，则跳到下一个字符。
        if not notDoNext == 0:
            notDoNext = notDoNext - 1
            continue
        # 如果有特殊标记，则进入特殊标记检查，否则正常加上。
        if originalString[pointNumber] == "\\":
            # 后面跟v就调变量，后面跟c就加颜色，后面跟f就清颜色，后面跟\就加\，都不是就错误。
            try:
                if originalString[pointNumber + 1] == "v":
                    returnValue = returnValue + str(stringVariable[useVariableCount])
                    useVariableCount = useVariableCount + 1
                    notDoNext = 1
                elif originalString[pointNumber + 1] == "s":
                    notDoNext = 1
                elif originalString[pointNumber + 1] == "c":
                    firstColor = originalString[pointNumber + 2]
                    secondColor = originalString[pointNumber + 3]
                    thirdColor = originalString[pointNumber + 4]
                    if firstColor == "?":
                        firstColor = None
                    if secondColor == "?":
                        secondColor = None
                    if thirdColor == "?":
                        thirdColor = None
                    returnValue = returnValue + ParseColor(firstColor, secondColor, thirdColor)
                    notDoNext = 4
                elif originalString[pointNumber + 1] == "f":
                    returnValue = returnValue + ParseColor("clear")
                    notDoNext = 1
                elif originalString[pointNumber + 1] == "\\":
                    returnValue = returnValue + "\\"
                    notDoNext = 1
                else:
                    Ferror.Error("String format error. From: " + originalString + ".")
            except:
                Ferror.Error("String format error. From: " + originalString + ".")
        else:
            returnValue = returnValue + originalString[pointNumber]
    return returnValue


# 解析颜色。
def ParseColor(colorName=None, backgroundName=None, wayName=None):
    # 若无输入则转为默认。
    if colorName is None:
        colorName = "8"
    if backgroundName is None:
        backgroundName = "1"
    if wayName is None:
        wayName = "1"
    # 若颜色名称是无，则返回清空属性，否则正常返回。
    if colorName == "clear":
        return "\033[0m"
    try:
        return "\033[" + wayDict[wayName] + ";" + colorDict[colorName] + ";" + backgroundDict[backgroundName] + "m"
    except:
        Ferror.Error("Color format error.")


# 读取一语言文件。
def ReadLang(dirPath):
    try:
        fileContent = Ffile.ReadFile(dirPath + "en_us.slang")
        splitByLine = fileContent.split("\n")
        lineNum = len(splitByLine)
        for lineNow in range(0, lineNum):
            singleLine = splitByLine[lineNow]  # 本行内容。
            lineLen = len(singleLine)  # 本行长度。
            # 如果是空行，则跳过。
            if lineLen == 0:
                continue
            # 如果是注释，则跳过。
            if singleLine[0] == "#":
                continue
            charNow = 0
            langID = ""
            langContent = ""
            isInvalid = False
            # 分出来语言标识符。
            while True:
                if charNow == lineLen:
                    isInvalid = True
                    break
                if singleLine[charNow] == "=":
                    charNow = charNow + 1
                    break
                langID = langID + singleLine[charNow]
                charNow = charNow + 1
            # 分出来语言行内容。
            while True:
                if charNow == lineLen:
                    break
                langContent = langContent + singleLine[charNow]
                charNow = charNow + 1
            # 如果不合法，则注释并跳过。
            if langID == "" or isInvalid:
                splitByLine[lineNow] = "#" + splitByLine[lineNow]
                linePrompt = " (line " + str(lineNow + 1) + ")"
                Flog.WriteLog(logName, "File format error. From: " + dirPath + "en_us.slang" + linePrompt + ".", 2)
                continue
            # 添加进Original（英语）映射表里。
            langDictOriginal.setdefault(langID, langContent)
    except:
        Ferror.Error("File format error. From: " + dirPath + "en_us.slang")
    try:
        fileContent = Ffile.ReadFile(dirPath + currentLang + ".slang")
        splitByLine = fileContent.split("\n")
        lineNum = len(splitByLine)
        for lineNow in range(0, lineNum):
            singleLine = splitByLine[lineNow]  # 本行内容。
            lineLen = len(singleLine)  # 本行长度。
            # 如果是空行，则跳过。
            if lineLen == 0:
                continue
            # 如果是注释，则跳过。
            if singleLine[0] == "#":
                continue
            charNow = 0
            langID = ""
            langContent = ""
            isInvalid = False
            # 分出来语言标识符。
            while True:
                if charNow == lineLen:
                    isInvalid = True
                    break
                if singleLine[charNow] == "=":
                    charNow = charNow + 1
                    break
                langID = langID + singleLine[charNow]
                charNow = charNow + 1
            # 分出来语言行内容。
            while True:
                if charNow == lineLen:
                    break
                langContent = langContent + singleLine[charNow]
                charNow = charNow + 1
            # 如果不合法，则注释并跳过。
            if langID == "" or isInvalid:
                splitByLine[lineNow] = "#" + splitByLine[lineNow]
                linePrompt = " (line " + str(lineNow + 1) + ")"
                Flog.WriteLog(logName,
                              "File format error. From: " + dirPath + currentLang + ".slang" + linePrompt + ".", 2)
                continue
            # 添加进Default（用户设置语言）映射表里。
            langDictDefault.setdefault(langID, langContent)
    except:
        Flog.WriteLog(logName, "File format error. From: " + dirPath + currentLang + ".slang", 2)


# 初始化系统语言文件。
def InitSystemLang():
    Flog.WriteLog(logName, "Start: load system languages.", 3)
    # 从配置文件获取语言。
    global currentLang
    currentLang = Fconfig.GetConfigValue("config/global.scfg", "language")
    # 读取语言。
    ReadLang("apis/lang/")
    Flog.WriteLog(logName, "End: load system languages.", 3)
