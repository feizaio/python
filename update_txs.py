import subprocess
import shutil
import os
import datetime
import glob
import re
import sys

# 获取当前系统时间并格式化
current_datetime = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")

vs_path = r"C:\\Program Files\\Microsoft Visual Studio\\2022\\Enterprise\\Common7\\IDE\\devenv"
sln_path = r"C:\\ProgramData\\Jenkins\\.jenkins\\workspace\\tuxinshuo\\TuXinEarthPlugins.sln"
# 使用Visual Studio重新构建解决方案
build_command = f'"{vs_path}" "{sln_path}" /Rebuild'

result = subprocess.run(build_command, shell=True, capture_output=True, text=True)
output = result.stdout
match = re.search(r"(\d+) 失败", output)
print(output)
if match and int(match.group(1)) > 0:
        print("编译失败")
        sys.exit(1)


# 复制文件和目录
shutil.copy("C:\\ProgramData\\Jenkins\\.jenkins\\workspace\\tuxinshuo\\图新说.exe", "E:\\source\\service")
shutil.copytree("C:\\ProgramData\\Jenkins\\.jenkins\\workspace\\tuxinshuo\\BIN", "E:\\source\\service\\BIN")
shutil.copytree("C:\\ProgramData\\Jenkins\\.jenkins\\workspace\\tuxinshuo\\Resources", "E:\\source\\service\\Resources")

# 切换到BIN目录
os.chdir("E:\\source\\service\\BIN")

# 删除bin目录下的所有*.pdb文件
for file in glob.glob("**/*.pdb", recursive=True):
    try:
        os.remove(file)
    except FileNotFoundError:
        pass  # 如果文件不存在，则忽略该错误

# 删除bin目录下的TempDir文件夹
try:
    shutil.rmtree("E:\\source\\service\\BIN\\TempDir")
except FileNotFoundError:
    pass  # 如果目录不存在，则忽略该错误

# 删除bin目录下的ModelLibrary文件夹
try:
    shutil.rmtree("E:\\source\\service\\BIN\\Plugins\\TuXinEarth.Feature\\ModelLibrary")
except FileNotFoundError:
    pass
# 删除bin目录下的ModelLibraryTemp文件夹
try:
    shutil.rmtree("E:\\source\\service\\BIN\\Plugins\\TuXinEarth.Feature\\ModelLibraryTemp")
except FileNotFoundError:
    pass

# 重命名ModelLibrary-Official为ModelLibrary
os.chdir("E:\\source\\service\\BIN\\Plugins\\TuXinEarth.Feature")
os.rename("ModelLibrary-Official","ModelLibrary")
# 删除bin目录下的debug.log和hardinfo.log文件
try:
    os.remove("E:\\source\\service\\BIN\\debug.log")
    os.remove("E:\\source\\service\\BIN\\hardinfo.log")
except FileNotFoundError:
    pass  # 如果文件不存在，则忽略该错误

# 删除BIN\packages\GlobeDll目录下的glVersion.txt、LocaLog.txt和GeoScene文件夹
try:
    os.remove("E:\\source\\service\\BIN\\packages\\GlobeDll\\glVersion.txt")
    os.remove("E:\\source\\service\\BIN\\packages\\GlobeDll\\LocaLog.txt")
    shutil.rmtree("E:\\source\\service\\BIN\\packages\\GlobeDll\\GeoScene")
    os.remove("E:\\source\\service\\BIN\\packages\\TuXinEarthDll\\TuXinEarth.Core.txt")
    os.remove("E:\\source\\service\\BIN\\packages\\GlobeDll\\Resource\\offlineData.txs")
except FileNotFoundError:
    pass  # 如果文件或目录不存在，则忽略该错误

# 根据Choice Parameter的值来决定是否删除特殊文件夹
jenkins_choice = os.environ.get("发布环境")

if jenkins_choice == "master":
    try:
        # 删除BIN\Plugins\TuXinEarth.BasePlugin.json
        os.remove("E:\\source\\service\\BIN\\Plugins\\TuXinEarth.BasePlugin.json")
        # 删除BIN\packages\TuXinEarthDll\TuXinEarth.Authentication.json
        os.remove("E:\\source\\service\\BIN\\packages\\TuXinEarthDll\\TuXinEarth.Authentication.json")
        os.remove("E:\\source\\service\\BIN\\packages\\TuXinEarth.DownLoadFile.exe.json")
        os.remove("E:\\source\\service\\BIN\\packages\\TuXinEarth.UploadingManager.exe.json")
    except FileNotFoundError:
        pass  # 如果文件不存在，则忽略该错误


# 根据Choice Parameter的值来决定压缩包路径
if jenkins_choice == "master":
    destination_path = "E:\\source\\master"
elif jenkins_choice == "developer":
    destination_path = "E:\\source\\developer"
else:
    print("未知的发布环境")
    sys.exit(1)

# 使用7-Zip压缩文件
subprocess.call([
    "C:\\Program Files\\7-Zip\\7z.exe",
    "a",
    os.path.join(destination_path, f"图新说-{current_datetime}.zip"),
    "E:\\source\\service\\BIN",
    "E:\\source\\service\\Resources",
    "E:\\source\\service\\图新说.exe"
])

# 重命名文件
os.chdir("E:\\source\\service")
os.rename("readme.txt", os.path.join(destination_path, f"图新说-{current_datetime}.txt"))

# 删除目录
shutil.rmtree("E:\\source\\service\\BIN")
shutil.rmtree("E:\\source\\service\\Resources")
os.remove("E:\\source\\service\\图新说.exe")
