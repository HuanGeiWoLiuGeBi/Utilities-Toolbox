import importlib as Eimportlib
import types as Etypes

import apis.basic.const as Bconst
import apis.frame.file as Ffile
import apis.frame.log as Flog
import apis.frame.warning as Fwarning

logName = "Frame-Register"

allGroupInfo = []  # 所有组的信息。
allFunctionInfo = []  # 所有函数的信息。


# 获取所有可用函数名称。
def GetAllFunctionName():
    returnValue = []
    for singleFunctionInfo in allFunctionInfo:
        returnValue.append(singleFunctionInfo[0] + "-" + singleFunctionInfo[1])
    return returnValue


# 获取所有可用函数。
def GetAllFunction():
    returnValue = []
    for singleFunctionInfo in allFunctionInfo:
        returnValue.append([singleFunctionInfo[0] + "-" + singleFunctionInfo[1], singleFunctionInfo[2]])
    return returnValue


# 注册功能。
def RegisterFunction():
    # 检查一个功能。
    def CheckFunction(groupDir, functionDir, informationFormatVersionCode):
        Tfunction = Eimportlib.import_module("functions." + groupDir + "." + functionDir + ".main")
        if informationFormatVersionCode == 1:
            allFunctionInfo.append([groupDir, functionDir, Tfunction.Start])

    # 检查一个组。
    def CheckGroup(groupDir):
        Tgroup = Eimportlib.import_module("functions." + groupDir + ".init")  # 引用组。
        groupInfo = Tgroup.GetGroupInfo()  # 组信息。
        programVersionCode = Bconst.GetValue("programVersionCode")  # 现在程序版本。
        informationFormatVersionCode = groupInfo[0]  # 组格式版本。
        if informationFormatVersionCode == 1:
            # 1格式：信息格式版本；最低程序版本；组版本；组名；组作者；组链接；组介绍；组详细介绍；组功能列表；组预加载函数。
            if not (type(groupInfo[0]) == int and type(groupInfo[1]) == int and type(groupInfo[2]) == int and type(
                    groupInfo[3]) == str and type(groupInfo[4]) == str and type(groupInfo[5]) == str and type(
                groupInfo[6]) == str and type(groupInfo[7]) == list and type(groupInfo[8]) == list and type(
                groupInfo[9]) == Etypes.FunctionType):
                Flog.WriteLog(logName, "Failed to load group - " + groupDir + ": group information error.", 1)
                Fwarning.warningList.append(["apis.frame.register.failed_load_group", [groupDir]])
                raise
            # 将组的信息更加可视化。
            minSupportProgramVersionCode = groupInfo[1]
            groupVersionCode = groupInfo[2]
            groupName = groupInfo[3]
            groupAuthor = groupInfo[4]
            groupLink = groupInfo[5]
            groupDescription = groupInfo[6]
            groupDetailDescription = groupInfo[7]
            groupFunctionList = groupInfo[8]
            groupPreloadFunction = groupInfo[9]
            # 如果需要程序版本大于当前版本，则报错。
            if programVersionCode < minSupportProgramVersionCode:
                Flog.WriteLog(logName, "Failed to load group - " + groupDir + ": please update the program.", 1)
                Fwarning.warningList.append(["apis.frame.register.failed_load_group", [groupDir]])
                raise
            # 预加载，如果无法预加载，则报错。
            try:
                groupPreloadFunction()
            except:
                Flog.WriteLog(logName, "Failed to load group  - " + groupDir + ": preload error.", 1)
                Fwarning.warningList.append(["apis.frame.register.failed_load_group", [groupDir]])
                raise
            # 加载每一个功能。
            for singleFunction in groupFunctionList:
                try:
                    Flog.WriteLog(logName, "Start: load function - " + singleFunction + ".", 3)
                    CheckFunction(groupDir, singleFunction, 1)
                    Flog.WriteLog(logName, "End: load function - " + singleFunction + ".", 3)
                except:
                    Flog.WriteLog(logName, "Failed to load function - " + singleFunction + ".", 1)
                    Fwarning.warningList.append(
                        ["apis.frame.register.failed_load_function", [groupDir, singleFunction]])
            # 将组信息添加：路径；名称；版本；作者；链接；描述；详细描述。
            allGroupInfo.append([groupDir, groupName, groupVersionCode, groupAuthor, groupLink, groupDescription,
                                 groupDetailDescription])
        else:
            Flog.WriteLog(logName, "Failed to load group - " + groupDir +
                          ": unsupported information format, please update the program.", 1)
            raise

    # 获取functions文件夹中的所有合法文件夹。
    Flog.WriteLog(logName, "Start: load groups and functions.", 3)
    # 新建组列表文件。
    Ffile.NewFile("config/external_group.txt")
    # 未经验证的所有组。
    allGroupPre = Ffile.ReadFile("config/external_group.txt").split("\n")
    allGroupPre.insert(0, "system")
    # 所有组。
    allGroup = []
    # 判断未经验证的所有组是否合法。
    for singleGroup in allGroupPre:
        if singleGroup == "":
            continue
        if Ffile.IsDirExists("functions/" + singleGroup):
            allGroup.append(singleGroup)
        else:
            Flog.WriteLog(logName, "Failed to load group - " + singleGroup + ".", 1)
            Fwarning.warningList.append(["apis.frame.register.failed_load_group", [singleGroup]])
    # 逐个加载组，顺带判断合法性。
    for singleGroup in allGroup:
        try:
            Flog.WriteLog(logName, "Start: load group - " + singleGroup + ".", 3)
            CheckGroup(singleGroup)
            Flog.WriteLog(logName, "End: load group - " + singleGroup + ".", 3)
        except:
            Flog.WriteLog(logName, "Failed to load group - " + singleGroup + ".", 1)
            Fwarning.warningList.append(["apis.frame.register.failed_load_group", [singleGroup]])
    Flog.WriteLog(logName, "End: load groups and functions.", 3)
