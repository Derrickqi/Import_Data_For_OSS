# Import_Data_For_OSS



"""
此脚本用于从云oss系统上传/下载/展示文件!
在使用它之前，您应该确保python有包:oss2
安装方式:pip install oss2

Usage:
  Downlaod files:
    python download_from_oss.py -f file1 -f file2 -o ./dest/
  Show fileLists on the oss:
    python download_from_oss.py -l
  Upload file to the oss:
    python download_from_oss.py -f ./file1 -f ./file2 -p log/test1 --upload

NOTES:
1. When the mode is Show files '-l' , other args is not used.
2. When the mode is download files, '-f' appended with the file name on the oss,
    you can check the name by show fileLists on the oss.
    The '-o' means save the files at local path.
3. When the mode is upload files, '-f' means the files at local machine,
    '-p' means the prefix you want add to the filename on the oss,
    this is the way to distinguish the different floder.
4. When you using internal networks! You should use '-i' argument,
    just for free transform.

"""

#注:此脚本摘自腾讯云

.
