import os as Eos
import shutil as Eshutil
import zipfile as Ezipfile

logName = "Frame-File"


# 删除整个目录。
def DeleteDir(dirPath):
    # 删除整个目录
    try:
        Eshutil.rmtree(dirPath)
    except:
        pass


# 删除一个文件。
def DeleteFile(filePath):
    # 删除文件。
    try:
        Eos.remove(filePath)
    except:
        pass


# 删除目录或文件。
def DeleteSomething(somethingPath):
    DeleteFile(somethingPath)
    DeleteDir(somethingPath)


# 获取文件所在文件夹路径。
def GetParentDir(filePath, levelNum=1):  # 文件路径；获取路径层数。
    returnValue = filePath
    # 循环levelNum遍。
    for countVariable in range(0, levelNum):
        # 获取上一级目录。
        returnValue = Eos.path.dirname(returnValue)
    return returnValue


# 查看文件是否存在。
def IsFileExists(filePath):
    return Eos.path.exists(filePath) and Eos.path.isfile(filePath)


# 查看文件夹是否存在。
def IsDirExists(dirPath):
    return Eos.path.exists(dirPath) and Eos.path.isdir(dirPath)


# 查看该路径是否被占用。
def IsSomethingExists(somethingPath):
    return Eos.path.exists(somethingPath)


# 创建一个目录。
def NewDir(dirPath):
    # 若已有目录，则不再创建。
    if IsDirExists(dirPath):
        return
    # 尝试正常创建目录。
    deleteLevel = 0  # 删除文件目录层数
    while True:
        # 尝试删除该文件。
        DeleteFile(GetParentDir(dirPath, deleteLevel))
        # 再次尝试，成功则返回，不成功继续查找。
        try:
            Eos.makedirs(dirPath)
            break
        except:
            deleteLevel = deleteLevel + 1
            pass


# 创建一个文件。
def NewFile(filePath, defaultContent="", encodingType="utf-8"):
    # 若已经是文件，则返回。
    if IsFileExists(filePath):
        return
    # 创建一个到此文件的目录。
    NewDir(GetParentDir(filePath))
    # 若是目录，删除此目录，继续创建。
    if IsDirExists(filePath):
        DeleteDir(filePath)
    # 写入文件
    with open(filePath, "w", encoding=encodingType) as fileContent:
        fileContent.write(defaultContent)


# 修改一个文件。
def ChangeFile(filePath, newContent, encodingType="utf-8"):
    try:
        # 尝试打开并读取，正常则写入内容，不正常则过。
        with open(filePath, "w", encoding=encodingType) as fileContent:
            fileContent.write(newContent)
    except:
        pass


# 向文件添加内容。
def AddFileContent(filePath, addContent, encodingType="utf-8"):
    try:
        # 尝试打开并读取，正常则添加内容，不正常则过。
        with open(filePath, "a", encoding=encodingType) as fileContent:
            fileContent.write(addContent)
    except:
        pass


# 读取文件。
def ReadFile(filePath, encodingType="utf-8"):
    try:
        # 尝试打开并读取，正常则返回内容，不正常则不返回。
        with open(filePath, "r", encoding=encodingType) as fileContent:
            returnValue = fileContent.read()
        return returnValue
    except:
        return ""


# 查看特定编码的文件是否可读。
def CanRead(filePath, encodingType="utf-8"):
    try:
        # 尝试打开并读取，正常则返回可读，不正常则返回不可读。
        with open(filePath, "r", encoding=encodingType) as fileContent:
            tempVarible = fileContent.read()
            return True
    except:
        return False


def UnZip(filePath, afterPath):
    try:
        # 新建路径。
        NewDir(GetParentDir(afterPath))
        # 解压。
        zipFile = Ezipfile.ZipFile(filePath)
        zipFile.extractall(afterPath)
        return True
    except:
        return False


def CopySomething(sourcePath, targetPath):
    try:
        # 删除目标路径。
        DeleteSomething(targetPath)
        # 新建路径。
        NewDir(GetParentDir(targetPath))
        # 粘贴。
        Eshutil.copytree(sourcePath, targetPath)
        return True
    except:
        return False
