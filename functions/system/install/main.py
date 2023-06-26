import os as Eos

import apis.frame.check as Fcheck
import apis.frame.file as Ffile
import apis.frame.io as Fio

logName = "Functions-System-Install"
displayName = "functions.system.install.name"
vaildGroupNameChar = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s",
                      "t", "u", "v", "w", "x", "y", "z", "1", "2", "3", "4", "5", "6", "7", "8", "9", "0", "_"]


# 获取组列表。
def GetList():
    fileContent = Ffile.ReadFile("config/external_group.txt")
    groupList = fileContent.split("\n")  # 原列表。
    afterGroupList = []  # 筛选合法值后的列表。
    for singleGroup in groupList:
        # 如果是空行，就跳过。
        if singleGroup == "" or singleGroup == "system":
            continue
        # 如果已经有同样的内容了，就跳过。
        if singleGroup in afterGroupList:
            continue
        # 如果有不合法字符，就跳过。
        if not Fcheck.StringCheck(singleGroup, vaildGroupNameChar):
            continue
        # 加入组名称。
        afterGroupList.append(singleGroup)
    return afterGroupList


# 应用组列表。
def ApplyList(groupList):
    fileContent = ""
    for singleGroup in groupList:
        fileContent = fileContent + singleGroup + "\n"
    Ffile.ChangeFile("config/external_group.txt", fileContent)


# 添加组。
def AddGroup(groupName):
    allGroup = GetList()
    if groupName in allGroup:
        return False
    allGroup.append(groupName)
    ApplyList(allGroup)
    return True


# 移除组。
def RemoveGroup(groupName):
    allGroup = GetList()
    if groupName not in allGroup:
        return False
    allGroup.remove(groupName)
    ApplyList(allGroup)
    return True


# 安装一个组。
def Install():
    # 输入要安装的组的路径。
    filePath = Fio.InputValue(displayName, None, "functions.system.install.input.ask_path_install")
    # 清空原暂存路径。
    Ffile.DeleteSomething("libs/system/install/temp/")
    # 操作是否成功。
    isValid = Ffile.UnZip(filePath, "libs/system/install/temp/")
    # 不成功则输出失败。
    if not isValid:
        Fio.PrintText(displayName, "functions.system.install.output.cant_extract_file")
        return
    # 提取这里面的所有组。
    allGroup = Eos.listdir("libs/system/install/temp/")
    # 安装的组的列表。
    installList = ""
    # 遍历每个要安装的组。
    for singleGroup in allGroup:
        # 如果名称是系统或已经有过这个组，就不装了。
        if singleGroup == "system" or singleGroup in GetList():
            continue
        # 删除要去安装的路径的文件。
        Ffile.DeleteSomething("functions/" + singleGroup)
        # 复制文件。
        Ffile.CopySomething("libs/system/install/temp/" + singleGroup, "functions/" + singleGroup)
        # 更新组列表。
        AddGroup(singleGroup)
        # 更新成功安装的组字符串。
        installList = installList + singleGroup + ","
    # 清空缓存。
    Ffile.DeleteSomething("libs/system/install/temp/")
    # 输出提示信息。
    if installList == "":
        Fio.PrintText(displayName, "functions.system.install.output.no_group_install")
    else:
        Fio.PrintText(displayName, "functions.system.install.output.complete_install", [installList[0:-1]])


# 卸载一个组。
def Uninstall():
    groupName = Fio.InputValue(displayName, None, "functions.system.install.input.ask_path_uninstall")
    statusFlag = RemoveGroup(groupName)
    if statusFlag:
        Fio.PrintText(displayName, "functions.system.install.output.complete_uninstall", [groupName])
    else:
        Fio.PrintText(displayName, "functions.system.install.output.uninstall_failed", [groupName])


# 开始函数。
def Start():
    # 询问要安装还是卸载。
    Fio.PrintText(displayName, "functions.system.install.input_pro.ask_way_1")
    Fio.PrintText(displayName, "functions.system.install.input_pro.ask_way_2")
    userInput = Fio.InputValue(displayName, ["Install", "Uninstall"], "functions.system.install.input.ask_way")
    if userInput == "Install":
        Install()
    else:
        Uninstall()
