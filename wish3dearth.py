import codecs
import os
import shutil
import zipfile
import subprocess
import re

#更新代码
os.chdir(r"D:\\CODE\\Wish3DEarthBuilder-2.0.0")
os.system("svn update  --username chentt --password ctt123456 --trust-server-cert")

with codecs.open("D:\\CODE\\Wish3DEarthBuilder-2.0.0\\Src\\Common\\GSFile.cpp", "r", encoding="gb2312") as file:
    lines = file.readlines()

for i, line in enumerate(lines):
    if "m_strProductVersion" in line:
        version_string = line.split("=")[1].strip().strip('";')
        version_number = version_string.split(".")[-1]
        #获取新版本号变量
        new_version_number = os.environ.get('版本号')
        #替换版本号为新版本号
        lines[i] = line.replace(version_number, new_version_number)
        break

#重写
with codecs.open("D:\\CODE\\Wish3DEarthBuilder-2.0.0\\Src\\Common\\GSFile.cpp", "w", encoding="gb2312") as file:
    file.writelines(lines)

#编译
vs_path = r"C:\\Program Files (x86)\\Microsoft Visual Studio\\2017\\Professional\\Common7\\IDE\\devenv"
sln_path = r"D:\\CODE\Wish3DEarthBuilder-2.0.0\\Builds\\32_x86_win_vc14\\GeoSceneFull.sln"
rebuild_command = f'"{vs_path}" "{sln_path}" /Rebuild'
build_command = f'"{vs_path}" "{sln_path}" /Build'

max_attempts = 10
attempts = 1
while attempts <= max_attempts:
    if attempts == 1:
        result = subprocess.run(rebuild_command, shell=True, capture_output=True, text=True)
    else:
        result = subprocess.run(build_command, shell=True, capture_output=True, text=True)
    output = result.stdout
    print(f"第 {attempts} 次编译日志:")
    print(output)
    match = re.search(r"失败 (\d+)", output)
    if match and int(match.group(1)) == 0:
        print("编译通过")
        break
    else:
        print(f"第 {attempts} 次编译失败，重新编译")
        attempts += 1

#jar包生成
os.chdir(r"D:\\CODE\\Wish3DEarthBuilder-2.0.0\\Product\\LocaspaceBuilder\\src\\LocaspaceBuilder")
os.system('"C:\\Program Files\\Java\\jdk1.8.0_191\\bin\\javac" -encoding UTF-8 -d D:\\CODE\\Wish3DEarthBuilder-2.0.0\\Product\\LocaspaceBuilder\\out\\production\\LocaspaceBuilder *.java')

os.chdir(r"D:\\CODE\\Wish3DEarthBuilder-2.0.0\\Product\\LocaspaceBuilder\\out\\production")
os.system('"C:\\Program Files\\Java\\jdk1.8.0_191\\bin\\jar" cvfm LocaspaceBuilder.jar LocaspaceBuilder\\META-INF\\MANIFEST.MF -C LocaspaceBuilder/ .')

#打包
folder_name = f"LocaspaceBuilder-2.0.0.{new_version_number}"

#指定路径
path = "D:\\publish\\Wish3DEarthBuilder-2.0.0"

#创建文件夹
folder_path = os.path.join(path, folder_name)
if not os.path.exists(folder_path):
    os.mkdir(folder_path)
    print(f"文件夹 {folder_path} 创建成功")
else:
    print(f"文件夹 {folder_path} 已存在")


def copy_dll_files(source_dir, dest_dir):
    if not os.path.exists(dest_dir):
        os.makedirs(dest_dir)

    for file_name in os.listdir(source_dir):
        source_file = os.path.join(source_dir, file_name)
        if os.path.isfile(source_file) and file_name.endswith('.dll'):
            shutil.copy(source_file, dest_dir)


def zip_folder(folder_path, output_path):
    with zipfile.ZipFile(output_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, _, files in os.walk(folder_path):
            for file in files:
                file_path = os.path.join(root, file)
                zipf.write(file_path, os.path.relpath(file_path, folder_path))
#源路径和目标路径
dll_source_dir = r'D:\\CODE\\Wish3DEarthBuilder-2.0.0\\Builds\\32_x86_win_vc14\\Bin_x64'
resource_source_dir = os.path.join(dll_source_dir, 'Resource')
jar_source_file = r'D:\\CODE\\Wish3DEarthBuilder-2.0.0\\Product\\LocaspaceBuilder\\out\\production\\LocaspaceBuilder.jar'
locaspace_builder_dir = r'D:\\publish\\Wish3DEarthBuilder-2.0.0\\temporary'
bin64 = r'D:\\publish\\Wish3DEarthBuilder-2.0.0\\temporary\\Bin_64'
#创建目录
os.makedirs(locaspace_builder_dir, exist_ok=True)
copy_dll_files(resource_source_dir, bin64)

#将LocaspaceBuilder.jar复制到LocaspaceBuilder-2.0.0.xxx文件夹
shutil.copy(jar_source_file, locaspace_builder_dir)
zip_path = fr'D:\\publish\\Wish3DEarthBuilder-2.0.0\\LocaspaceBuilder-2.0.0.{new_version_number}\\LocaspaceBuilder-2.0.0.{new_version_number}.zip'
zip_folder(locaspace_builder_dir,zip_path)
#删除临时文件夹
shutil.rmtree(locaspace_builder_dir)
shutil.rmtree(jar_source_file)