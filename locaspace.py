import os
import codecs
import re
import shutil
import zipfile
import subprocess
#更新代码
os.chdir(r"D:\\CODE\\LocaSpace-7.2.1")
os.system("svn update  --username lihao --password lihao --trust-server-cert")

#修改GSFile.cpp版本号
with codecs.open("D:\\CODE\\LocaSpace-7.2.1\\Src\\Common\\GSFile.cpp", "r", encoding="utf-8") as file:
    lines = file.readlines()
for i, line in enumerate(lines):
    if "m_strProductVersion" in line:
        version_string = line.split("=")[1].strip().strip('";')
        version_number = version_string.split(".")[-1]
        GSFile_new_version_number = os.environ.get('GSFile版本号')
        lines[i] = line.replace(version_number, GSFile_new_version_number)
        break
with codecs.open("D:\\CODE\\LocaSpace-7.2.1\\Src\\Common\\GSFile.cpp", "w", encoding="utf-8") as file:
    file.writelines(lines)

#修改GSGlobeDotNet.rc版本号
version_file_path = 'D:\\CODE\\LocaSpace-7.2.1\\Product\\DotNetComponent\\GSGlobeDotNet\\GSGlobeDotNet.rc'
GSGlobeDotNet_new_version_number = os.environ.get('GSGlobeDotNet版本号')
with open(version_file_path, 'r',encoding="gb2312") as file:
    version_file_content = file.read()
version_pattern = r"FILEVERSION \d,\d,\d,(\d+)"
match = re.search(version_pattern, version_file_content)
if match:
    old_version_number = match.group(1)
with open(version_file_path, 'r', encoding='gb2312') as file:
    app_rc_file_content = file.read()
app_rc_file_content = re.sub(r"VALUE \"ProductVersion\", \"7.2.0.\d+\"", f"VALUE \"ProductVersion\", \"7.2.0.{GSGlobeDotNet_new_version_number}\"", app_rc_file_content)
app_rc_file_content = re.sub(r"VALUE \"FileVersion\", \"7.2.0.\d+\"", f"VALUE \"FileVersion\", \"7.2.0.{GSGlobeDotNet_new_version_number}\"", app_rc_file_content)
app_rc_file_content = re.sub(r"FILEVERSION 7,2,0,\d+", f"FILEVERSION 7,2,0,{GSGlobeDotNet_new_version_number}", app_rc_file_content)
app_rc_file_content = re.sub(r"PRODUCTVERSION 7,2,0,\d+", f"PRODUCTVERSION 7,2,0,{GSGlobeDotNet_new_version_number}", app_rc_file_content)
with open(version_file_path, 'w', encoding='gb2312') as file:
    file.write(app_rc_file_content)

#编译
vs_path = r"C:\\Program Files (x86)\\Microsoft Visual Studio\\2017\\Professional\\Common7\\IDE\\devenv"
sln_path = r"D:\\CODE\\LocaSpace-7.2.1\\Builds\\32_x86_win_vc15\\GeoSceneFull.sln"
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
    print(f"第 {attempts} 次编译日志:")
    print(output)
    match = re.search(r"失败 (\d+)", output)
    if match and int(match.group(1)) == 0:
        print("编译通过")
        break
    else:
        print(f"第 {attempts} 次编译失败，重新编译")
        attempts += 1

#拷贝C#
def copy_files(source_dir, target_dir):
    resource_dir = os.path.join(source_dir, 'Resource')
    target_resource_dir = os.path.join(target_dir, 'Resource')
    os.makedirs(target_resource_dir, exist_ok=True)
    for root, dirs, files in os.walk(resource_dir):
        relative_path = os.path.relpath(root, resource_dir)
        target_subdir = os.path.join(target_resource_dir, relative_path)
        os.makedirs(target_subdir, exist_ok=True)
        for file_name in files:
            source_file = os.path.join(root, file_name)
            shutil.copy2(source_file, target_subdir)
    files_to_copy = [
        'CloudResource.rrs',
		'GSRFileResource.rrs',
		'GSRResource.rrs',
		'OceanResource.rrs',
		'GSBalloonExDotNet.xml',
		'GSBuilderDotNet.xml',
		'GSGlobeDotNet.xml',
		'GSToolTipDotNet.xml',
		'Balloon.dll',
		'BalloonEx.dll',
		'CADAccessorPlugin.dll',
		'Common.dll',
		'DataDownLoad.dll',
		'DataEngine.dll',
		'FbxImporter.dll',
		'Feature.dll',
		'FreeImage.dll',
		'gdal300.dll',
		'geos.dll',
		'geos_c.dll',
		'GeoSceneBuilder.dll',
		'Globe.dll',
		'GORasterAccessorPlugin.dll',
		'GOVectorAccessorPlugin.dll',
		'GSBalloonExDotNet.dll',
		'GSBuilderDotNet.dll',
		'GSGlobeDotNet.dll',
		'GSToolTipDotNet.dll',
		'KmlAccessorPlugin.dll',
		'laszip_api3.dll',
		'laszip3.dll',
		'LDBDataSource.dll',
		'LgdAccessorPlugin.dll',
		'libcurl.dll',
		'libexpat.dll',
		'libiconv.dll',
		'liblas.dll',
		'LidarAccessorPlugin.dll',
		'living1.dll',
		'LRPAccessorPlugin.dll',
		'mfc140.dll',
		'msvcp110.dll',
		'msvcp140.dll',
		'msvcr110.dll',
		'oci.dll',
		'ODBCDataSource.dll',
		'openvr_api.dll',
		'OracleDataSource.dll',
		'OsgAccessorPlugin.dll',
		'PointCloudConverter.dll',
		'proj_6_1.dll',
		'RasterDataAccessor.dll',
		'Render.dll',
		'RenderClouder.dll',
		'RenderDevice.dll',
		'RenderDeviceGL.dll',
		'RenderOcean.dll',
		'shp.dll',
		'SimplygonSDKRuntimeReleasex64.dll',
		'SketchUpAPI.dll',
		'SketchUpCommonPreferences.dll',
		'SkpAccessorPlugin.dll',
		'sqlite3.dll',
		'SqlServerDataSource.dll',
		'Toolkit.dll',
		'vcomp110.dll',
		'VecTileMaker.dll',
		'VectorDataAccessor.dll',
		'VersionInfoGL.dll',
		'Win32NetUtility.dll',
		'zlib.dll',
        'GltfAccessorPlugin.dll'
    ]
    for file_name in files_to_copy:
        shutil.copy2(os.path.join(source_dir, file_name), target_dir)

#拷贝C#
source_path = r'D:\\CODE\\LocaSpace-7.2.1\\Builds\\32_x86_win_vc15\\Bin_x64'
target_path = r'D:\\publish\\LocaSpace721\\temporary\\C#'
os.makedirs(target_path, exist_ok=True)
copy_files(source_path, target_path)

#拷贝C++/dll
def copy_files(source_dir, target_dir):
    resource_dir = os.path.join(source_dir, 'Resource')
    target_resource_dir = os.path.join(target_dir, 'Resource')
    os.makedirs(target_resource_dir, exist_ok=True)
    for root, dirs, files in os.walk(resource_dir):
        relative_path = os.path.relpath(root, resource_dir)
        target_subdir = os.path.join(target_resource_dir, relative_path)
        os.makedirs(target_subdir, exist_ok=True)
        for file_name in files:
            source_file = os.path.join(root, file_name)
            shutil.copy2(source_file, target_subdir)
    files_to_copy = [
        'CloudResource.rrs',
        'GSRFileResource.rrs',
        'GSRResource.rrs',
        'OceanResource.rrs',
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
        'GORasterAccessorPlugin.dll',
        'GOVectorAccessorPlugin.dll',
        'KmlAccessorPlugin.dll',
        'laszip_api3.dll',
        'laszip3.dll',
        'LgdAccessorPlugin.dll',
        'libcurl.dll',
        'libexpat.dll',
        'libiconv.dll',
        'liblas.dll',
        'LidarAccessorPlugin.dll',
        'living1.dll',
        'LRPAccessorPlugin.dll',
        'mfc140.dll',
        'msvcp110.dll',
        'msvcp140.dll',
        'msvcr110.dll',
        'openvr_api.dll',
        'OsgAccessorPlugin.dll',
        'PointCloudConverter.dll',
        'proj_6_1.dll',
        'RasterDataAccessor.dll',
        'Render.dll',
        'RenderClouder.dll',
        'RenderDevice.dll',
        'RenderDeviceGL.dll',
        'RenderOcean.dll',
        'shp.dll',
        'SimplygonSDKRuntimeReleasex64.dll',
        'SketchUpAPI.dll',
        'SketchUpCommonPreferences.dll',
        'SkpAccessorPlugin.dll',
        'sqlite3.dll',
        'Toolkit.dll',
        'vcomp110.dll',
        'VecTileMaker.dll',
        'VectorDataAccessor.dll',
        'VersionInfoGL.dll',
        'Win32NetUtility.dll',
        'zlib.dll',
        'CADAccessorPlugin.dll',
        'GltfAccessorPlugin.dll'
    ]
    for file_name in files_to_copy:
        shutil.copy2(os.path.join(source_dir, file_name), target_dir)
source_path = r'D:\\CODE\\LocaSpace-7.2.1\\Builds\\32_x86_win_vc15\\Bin_x64'
target_path = r'D:\\publish\\LocaSpace721\\temporary\\C++\\dll'
os.makedirs(target_path, exist_ok=True)
copy_files(source_path, target_path)

#拷贝C++/include
def copy_files(source_dir, target_dir):
    folders_to_copy = ['Common', 'DataEngine', 'Feature', 'GeoSceneBuilder', 'Globe', 'RasterDataAccessor',
                      'Render', 'RenderDevice', 'Toolkit', 'VecTileMaker', 'VectorDataAccessor', 'VersionInfoGL']
    for folder_name in folders_to_copy:
        source_folder = os.path.join(source_dir, folder_name)
        target_folder = os.path.join(target_dir, folder_name)
        if os.path.exists(target_folder):
            shutil.rmtree(target_folder)
        shutil.copytree(source_folder, target_folder)
source_path = r'D:\\CODE\\LocaSpace-7.2.1\\Include'
target_path = r'D:\\publish\\LocaSpace721\\temporary\\C++\\include'
os.makedirs(target_path, exist_ok=True)
copy_files(source_path, target_path)

#拷贝C++/lib
def copy_files(source_dir, target_dir):
    files_to_copy = [
        'Common.lib',
        'DataEngine.lib',
        'Feature.lib',
        'GeoSceneBuilder.lib',
        'Globe.lib',
        'RasterDataAccessor.lib',
        'Render.lib',
        'RenderDevice.lib',
        'Toolkit.lib',
        'VecTileMaker.lib',
        'VectorDataAccessor.lib',
        'VersionInfoGL.lib'
    ]
    for file_name in files_to_copy:
        shutil.copy2(os.path.join(source_dir, file_name), target_dir)
source_path = r'D:\\publish\\LocaSpace721\\LocaSpace-SDK-7.2.0.1601-Beta\\C++\\lib'
target_path = r'D:\\publish\\LocaSpace721\\temporary\\C++\\lib'
os.makedirs(target_path, exist_ok=True)
copy_files(source_path, target_path)

#拷贝Test
def copy_files(source_dir, target_dir):
    resource_dir = os.path.join(source_dir, 'Resource')
    target_resource_dir = os.path.join(target_dir, 'Resource')
    os.makedirs(target_resource_dir, exist_ok=True)
    for root, dirs, files in os.walk(resource_dir):
        relative_path = os.path.relpath(root, resource_dir)
        target_subdir = os.path.join(target_resource_dir, relative_path)
        os.makedirs(target_subdir, exist_ok=True)
        for file_name in files:
            source_file = os.path.join(root, file_name)
            shutil.copy2(source_file, target_subdir)
    files_to_copy = [
        'CloudResource.rrs',
        'GSRFileResource.rrs',
        'GSRResource.rrs',
        'OceanResource.rrs',
        'GSBalloonExDotNet.xml',
        'GSBuilderDotNet.xml',
        'GSGlobeDotNet.xml',
        'GSToolTipDotNet.xml',
        'LocaSpace.exe',
        'Balloon.dll',
        'BalloonEx.dll',
        'CADAccessorPlugin.dll',
        'Common.dll',
        'DataDownLoad.dll',
        'DataEngine.dll',
        'DevComponents.DotNetBar2.dll',
        'FbxImporter.dll',
        'Feature.dll',
        'FreeImage.dll',
        'gdal300.dll',
        'geos.dll',
        'geos_c.dll',
        'GeoSceneBuilder.dll',
        'Globe.dll',
        'GORasterAccessorPlugin.dll',
        'GOVectorAccessorPlugin.dll',
        'GSBalloonExDotNet.dll',
        'GSBuilderDotNet.dll',
        'GSGlobeDotNet.dll',
        'GSToolTipDotNet.dll',
        'KmlAccessorPlugin.dll',
        'laszip_api3.dll',
        'laszip3.dll',
        'LDBDataSource.dll',
        'LgdAccessorPlugin.dll',
        'libcurl.dll',
        'libexpat.dll',
        'libiconv.dll',
        'liblas.dll',
        'LidarAccessorPlugin.dll',
        'living1.dll',
        'LRPAccessorPlugin.dll',
        'mfc140.dll',
        'msvcp110.dll',
        'msvcp140.dll',
        'msvcr110.dll',
        'oci.dll',
        'ODBCDataSource.dll',
        'openvr_api.dll',
        'OracleDataSource.dll',
        'OsgAccessorPlugin.dll',
        'PointCloudConverter.dll',
        'proj_6_1.dll',
        'RasterDataAccessor.dll',
        'Render.dll',
        'RenderClouder.dll',
        'RenderDevice.dll',
        'RenderDeviceGL.dll',
        'RenderOcean.dll',
        'shp.dll',
        'SimplygonSDKRuntimeReleasex64.dll',
        'SketchUpAPI.dll',
        'SketchUpCommonPreferences.dll',
        'SkpAccessorPlugin.dll',
        'sqlite3.dll',
        'SqlServerDataSource.dll',
        'Toolkit.dll',
        'vcomp110.dll',
        'VecTileMaker.dll',
        'VectorDataAccessor.dll',
        'VersionInfoGL.dll',
        'Win32NetUtility.dll',
        'ZedGraph.dll',
        'zlib.dll',
        'GltfAccessorPlugin.dll'
    ]
    for file_name in files_to_copy:
        shutil.copy2(os.path.join(source_dir, file_name), target_dir)
source_path = r'D:\\CODE\\LocaSpace-7.2.1\\Builds\\32_x86_win_vc15\\Bin_x64'
target_path = r'D:\\publish\\LocaSpace721\\temporary\\Test'
os.makedirs(target_path, exist_ok=True)
copy_files(source_path, target_path)


#打包
def zip_folder(folder_path, output_path):
    with zipfile.ZipFile(output_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, _, files in os.walk(folder_path):
            for file in files:
                file_path = os.path.join(root, file)
                zipf.write(file_path, os.path.relpath(file_path, folder_path))
source_folder = r'D:\\publish\\LocaSpace721\\temporary'
output_zip = fr'D:\\publish\\LocaSpace721\\LocaSpace-SDK-7.2.0.{GSFile_new_version_number}.zip'
zip_folder(source_folder, output_zip)
shutil.rmtree(r'D:\\publish\\LocaSpace721\\temporary')