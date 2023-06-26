import apis.frame.config as Fconfig
import apis.frame.lang as Flang


# 获取组信息。
def GetGroupInfo():
    informationFormatVersionCode = 1
    minSupportProgramVersionCode = 10
    groupVersionCode = 1
    groupName = "functions.system.name"
    groupAuthor = "functions.system.author"
    groupLink = "functions.system.link"
    groupDescription = "functions.system.description"
    groupDetailDescription = ["functions.system.detail_description_1", "functions.system.detail_description_2",
                              "functions.system.detail_description_3", "functions.system.detail_description_4",
                              "functions.system.detail_description_5"]
    groupFunctionList = ["clear", "help", "exit", "install", "restart"]
    groupPreloadFunction = PreLoad
    return [informationFormatVersionCode, minSupportProgramVersionCode, groupVersionCode, groupName, groupAuthor,
            groupLink, groupDescription, groupDetailDescription, groupFunctionList, groupPreloadFunction]


# 预加载函数。
def PreLoad():
    Flang.ReadLang("functions/system/lang/")
    Fconfig.CheckConfig("config/system/global.scfg", [
        ["exit_wait_time", "none", "3", "[0-9]{1,2}"]
    ])
