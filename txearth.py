import re
import os
import subprocess
import zipfile
import shutil

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
# Jenkins变量
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

#编译
vs_path = r"E:\\Software\\vs2022\\Common7\\IDE\\devenv"
sln_path = r"D:\\CODE\\TXEarth-SDK-1.1.0\\Builds\\vs2022\\TXEarth.sln"
rebuild_command = f'"{vs_path}" "{sln_path}" /Rebuild'
build_command = f'"{vs_path}" "{sln_path}" /Build'

#判定是否编译成功的次数
max_attempts = 10
attempts = 1

while attempts <= max_attempts:
    if attempts == 1:
        result = subprocess.run(rebuild_command, shell=True, capture_output=True, text=True)
    else:
        result = subprocess.run(build_command, shell=True, capture_output=True, text=True)

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

def copy_files(source_dir, target_dir):
    #拷贝Resource文件夹及其内部所有文件
    resource_dir = os.path.join(source_dir, 'Resource')
    target_resource_dir = os.path.join(target_dir, 'Resource')
    os.makedirs(target_resource_dir, exist_ok=True)
    for file_name in os.listdir(resource_dir):
        source_file = os.path.join(resource_dir, file_name)
        if os.path.isfile(source_file):
            shutil.copy2(source_file, target_resource_dir)

    #拷贝txePlugins文件夹及指定的文件
    plugins_dir = os.path.join(source_dir, 'txePlugins')
    target_plugins_dir = os.path.join(target_dir, 'txePlugins')
    os.makedirs(target_plugins_dir, exist_ok=True)
    shutil.copy2(os.path.join(plugins_dir, 'Plugin_FreeImage.dll'), target_plugins_dir)
    shutil.copy2(os.path.join(plugins_dir, 'Plugin_FreeType.dll'), target_plugins_dir)

    files_to_copy = [
        'TXEarthDotNet.xml',
        'boost_thread-vc141-mt-x64-1_76.dll',
        'Common.dll',
        'DataEngine.dll',
        'FbxImporter.dll',
        'Feature.dll',
        'FreeImage.dll',
        'gdal300.dll',
        'geos.dll',
        'geos_c.dll',
        'GeoSceneBuilder.dll',
        'Globe.dll',
        'KmlAccessorPlugin.dll',
        'libcurl.dll',
        'libexpat.dll',
        'libiconv.dll',
        'living1.dll',
        'LRPAccessorPlugin.dll',
        'msvcr110.dll',
        'openvr_api.dll',
        'OsgAccessorPlugin.dll',
        'proj_6_1.dll',
        'RasterDataAccessor.dll',
        'Render.dll',
        'RenderDevice.dll',
        'shp.dll',
        'sqlite3.dll',
        'System.Windows.Forms.dll',
        'Toolkit.dll',
        'txeAnalysis.dll',
        'TXEarthCpp.dll',
        'TXEarthDotNet.dll',
        'txeCommon.dll',
        'txeData.dll',
        'txeFeature.dll',
        'txeLayers.dll',
        'txeManipulator.dll',
        'txeRenderer.dll',
        'txeScene.dll',
        'txeViewer.dll',
        'txeWidgets.dll',
        'uv.dll',
        'VecTileMaker.dll',
        'VectorDataAccessor.dll',
        'zlib.dll',
    ]
    for file_name in files_to_copy:
        shutil.copy2(os.path.join(source_dir, file_name), target_dir)

#源路径和目标路径
source_path = r'D:\\CODE\\TXEarth-SDK-1.1.0\\Builds\\vs2022\\x64\\Release'
target_path = r'D:\\publish\TXEarth-SDK-1.1.0\\temporary'

os.makedirs(target_path, exist_ok=True)

#拷贝文件
copy_files(source_path, target_path)

#版本号文件夹名字
folder_name = f"TXEarth-SDK-1.1.0.{new_version_number}-x64"

#压缩包固定路径
path = "D:\\publish\\TXEarth-SDK-1.1.0"

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

#打包
source_folder = r'D:\\publish\TXEarth-SDK-1.1.0\\temporary'
output_zip = fr'D:\\publish\TXEarth-SDK-1.1.0\\TXEarth-SDK-1.1.0.{new_version_number}-x64\\TXEarth-SDK-1.1.0.{new_version_number}-x64.zip'

zip_folder(source_folder, output_zip)

shutil.rmtree(source_folder)
