import re
import os
import subprocess
import zipfile

# 更新代码
os.chdir(r"D:\\CODE\\TXEarth-SDK-1.1.0")
os.system("svn update  --username chentt --password ctt123456 --trust-server-cert")

# 路径
version_file_path = 'D:\\CODE\\TXEarth-SDK-1.1.0\\Core\\include\\Common\\Version.h'
app_rc_file_path = 'D:\\CODE\\TXEarth-SDK-1.1.0\\Packages\\.NET\\TXEarthDotNet\\app.rc'

# 读取Version.h
with open(version_file_path, 'r') as file:
    version_file_content = file.read()


version_pattern = r"#define TXE_VERSION_REVISION (\d+)"
match = re.search(version_pattern, version_file_content)

if match:
    old_version_number = match.group(1)

new_version_number = os.environ.get('版本号') 

version_pattern = r"#define TXE_VERSION_REVISION (\d+)"
new_version_line = f"#define TXE_VERSION_REVISION {new_version_number}"
# 替换Version.h版本号
version_file_content = re.sub(version_pattern, new_version_line, version_file_content)
with open(version_file_path, 'w') as file:
    file.write(version_file_content)

# 读取app.rc
with open(app_rc_file_path, 'r', encoding='utf-16-le') as file:
    app_rc_file_content = file.read()
# 替换app.rc版本号
app_rc_file_content = re.sub(r"VALUE \"ProductVersion\", \"1.1.0.\d+\"", f"VALUE \"ProductVersion\", \"1.1.0.{new_version_number}\"", app_rc_file_content)
app_rc_file_content = re.sub(r"VALUE \"FileVersion\", \"1.1.0.\d+\"", f"VALUE \"FileVersion\", \"1.1.0.{new_version_number}\"", app_rc_file_content)
app_rc_file_content = re.sub(r"FILEVERSION 1,1,0,\d+", f"FILEVERSION 1,1,0,{new_version_number}", app_rc_file_content)
app_rc_file_content = re.sub(r"PRODUCTVERSION 1,1,0,\d+", f"PRODUCTVERSION 1,1,0,{new_version_number}", app_rc_file_content)
with open(app_rc_file_path, 'w', encoding='utf-16-le') as file:
    file.write(app_rc_file_content)

# 编译
vs_path = r"E:\\Software\\vs2022\\Common7\\IDE\\devenv"
sln_path = r"D:\\CODE\\TXEarth-SDK-1.1.0\\Builds\\vs2022\\TXEarth.sln"
rebuild_command = f'"{vs_path}" "{sln_path}" /Rebuild'
build_command = f'"{vs_path}" "{sln_path}" /Build'

# 判定是否编译成功的次数
max_attempts = 10
attempts = 1

while attempts <= max_attempts:
    # 执行编译命令
    if attempts == 1:
        result = subprocess.run(rebuild_command, shell=True, capture_output=True, text=True)
    else:
        result = subprocess.run(build_command, shell=True, capture_output=True, text=True)

    # 获取编译结果输出
    output = result.stdout

    match = re.search(r"(\d+) 失败", output)
    if match and int(match.group(1)) == 0:
        print("编译通过")
        print(output)
        break
    else:
        print(f"第 {attempts} 次编译失败，重新编译")
        print(output)
        attempts += 1

# 构建文件夹名字
folder_name = f"TXEarth-SDK-1.1.0.{new_version_number}-x64"

# 指定路径
path = "D:\\publish\\TXEarth-SDK-1.1.0"

# 创建文件夹
folder_path = os.path.join(path, folder_name)
if not os.path.exists(folder_path):
    os.mkdir(folder_path)
    print(f"文件夹 {folder_path} 创建成功")
else:
    print(f"文件夹 {folder_path} 已存在")


def zip_folder(folder_path, output_path):
    with zipfile.ZipFile(output_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, _, files in os.walk(folder_path):
            for file in files:
                file_path = os.path.join(root, file)
                zipf.write(file_path, os.path.relpath(file_path, folder_path))

# 设置源文件夹和输出压缩包的路径
source_folder = r'D:\\CODE\\TXEarth-SDK-1.1.0\\Builds\\vs2022\\x64\\Release'
output_zip = fr'D:\\publish\TXEarth-SDK-1.1.0\\TXEarth-SDK-1.1.0.{new_version_number}-x64\\TXEarth-SDK-1.1.0.{new_version_number}-x64.zip'

# 打包文件夹
zip_folder(source_folder, output_zip)
