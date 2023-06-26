import apis.frame.lang as Flang
import apis.frame.io as Fio
import apis.frame.register as Fregister

displayName = "functions.system.help.name"
logName = "Functions-System-Help"


# 开始函数。
def Start():
    allGroup = Fregister.allGroupInfo
    # allGroupInfo.extend([groupDir, groupName, groupVersionCode, groupAuthor, groupLink, groupDescription, groupDetailDescription])
    for singleGroup in allGroup:
        Fio.PrintText(displayName, "functions.system.help.output.group_name", [Flang.FinalLang(singleGroup[1])])
        Fio.PrintText(displayName, "functions.system.help.output.group_version", [str(singleGroup[2])])
        Fio.PrintText(displayName, "functions.system.help.output.group_author", [Flang.FinalLang(singleGroup[3])])
        Fio.PrintText(displayName, "functions.system.help.output.group_link", [Flang.FinalLang(singleGroup[4])])
        Fio.PrintText(displayName, "functions.system.help.output.group_description",
                          [Flang.FinalLang(singleGroup[5])])
        Fio.PrintText(displayName, "functions.system.help.output.group_detail_description")
        for singleDescription in singleGroup[6]:
            Fio.PrintText(displayName, "functions.system.help.output.group_detail_description_line",
                              [Flang.FinalLang(singleDescription)])
