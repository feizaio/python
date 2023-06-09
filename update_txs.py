import subprocess
import shutil
import os
import datetime
import glob

# 获取当前系统时间并格式化
current_datetime = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")

# 切换到Visual Studio目录
os.chdir(r"C:\\Program Files\\Microsoft Visual Studio\\2022\\Enterprise\\Common7\\IDE")

# 使用Visual Studio重新构建解决方案
subprocess.call([
    "devenv",
    r"C:\\ProgramData\\Jenkins\\.jenkins\\workspace\\tuxinshuo\\TuXinEarthPlugins.sln",
    "/Rebuild"
])

# 复制文件和目录
shutil.copy("C:\\ProgramData\\Jenkins\\.jenkins\\workspace\\tuxinshuo\\图新说.exe", "E:\\source\\service")
shutil.copytree("C:\\ProgramData\\Jenkins\\.jenkins\\workspace\\tuxinshuo\\BIN", "E:\\source\\service\\BIN")
shutil.copytree("C:\\ProgramData\\Jenkins\\.jenkins\\workspace\\tuxinshuo\\Resources", "E:\\source\\service\\Resources")

# 切换到BIN目录
os.chdir("E:\\source\\service\\BIN")

# 删除bin目录下的所有*.pdb文件
for file in glob.glob("**/*.pdb", recursive=True):
    os.remove(file)

# 删除bin目录下的TempDir文件夹
shutil.rmtree("E:\\source\\service\\BIN\\TempDir")

# 删除bin目录下的debug.log和hardinfo.log文件
os.remove("E:\\source\\service\\BIN\\debug.log")
os.remove("E:\\source\\service\\BIN\\hardinfo.log")

# 删除BIN\packages\GlobeDll目录下的glVersion.txt、LocaLog.txt和GeoScene文件夹
os.remove("E:\\source\\service\\BIN\\packages\\GlobeDll\\glVersion.txt")
os.remove("E:\\source\\service\\BIN\\packages\\GlobeDll\\LocaLog.txt")
shutil.rmtree("E:\\source\\service\\BIN\\packages\\GlobeDll\\GeoScene")

# 根据Choice Parameter的值来决定是否删除特殊文件夹
jenkins_choice = os.environ.get("发布环境")

if jenkins_choice == "master":
    # 删除BIN\Plugins\TuXinEarth.BasePlugin.json
    os.remove("E:\\source\\service\\BIN\\Plugins\\TuXinEarth.BasePlugin.json")
    # 删除BIN\packages\TuXinEarthDll\TuXinEarth.Authentication.json
    os.remove("E:\\source\\service\\BIN\\packages\\TuXinEarthDll\\TuXinEarth.Authentication.json")

# 删除BIN\packages\GlobeDll\Resource目录下的offlineData.txs
os.remove("E:\\source\\service\\BIN\\packages\\GlobeDll\\Resource\\offlineData.txs")

# 使用7-Zip压缩文件
subprocess.call([
    "C:\\Program Files\\7-Zip\\7z.exe",
    "a",
    f"E:\\source\\service\\图新说-{current_datetime}.zip",
    "E:\\source\\service\\BIN",
    "E:\\source\\service\\Resources",
    "E:\\source\\service\\图新说.exe"
])

# 重命名文件
os.chdir("E:\\source\\service")
os.rename("readme.txt", f"图新说-{current_datetime}.txt")

# 删除目录
shutil.rmtree("E:\\source\\service\\BIN")
shutil.rmtree("E:\\source\\service\\Resources")
os.remove("E:\\source\\service\\图新说.exe")