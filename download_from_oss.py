# -*- coding: utf-8 -*-
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
from __future__ import print_function
import os,time,sys
import operator,oss2,argparse
from itertools import islice

FLAGS = None

# ------------------ 在这里设置您自己的信息 ------------------------
# 这些信息经常被使用。把它放在脚本的顶部
#                    AccessKeyId              AccessKeySecret
auth = oss2.Auth("AccessKeyId", "AccessKeySecret")
# 内部端点(参见oss控制面板)
endpoint = "http://内部端点"
# 公共端点
public_endpoint = "http://公共端点"
# Your bucket name
bucket_name = "Your bucket name"
# --------------------------------------------------------------------


def downloadFiles(bucket):
    """ downloadFiles
    download FLAGS.files on the oss
    """
    if not os.path.exists(FLAGS.outputPath):
        os.makedirs(FLAGS.outputPath)
        print("The floder {0} is not existed, will creat it".format(FLAGS.outputPath))

    start_time = time.time()
    for tmp_file in FLAGS.files:
        if not bucket.object_exists(tmp_file):
            print("File {0} is not on the OSS!".format(tmp_file))
        else:
            print("Will download {0} !".format(tmp_file))
            tmp_time = time.time()
            # cut the file name
            filename = tmp_file[tmp_file.rfind("/") + 1 : len(tmp_file)]
            localFilename = os.path.join(FLAGS.outputPath,filename)
            # bucket.get_object_to_file(
            oss2.resumable_download(
                bucket,
                tmp_file,
                localFilename,
                progress_callback = percentage)
            print("\nFile {0} -> {1} downloads finished, cost {2} Sec.".format(
                tmp_file, localFilename, time.time() - tmp_time ))

    print("All download tasks have finished!")
    print("Cost {0} Sec.".format(time.time() - start_time))

def uploadFiles(bucket):
    """ uploadFiles
    Upload FLAGS.files to the oss
    """
    start_time = time.time()
    for tmp_file in FLAGS.files:
        if not os.path.exists(tmp_file):
            print("File {0} is not exists!".format(tmp_file))
        else:
            print("Will upload {0} to the oss!".format(tmp_file))
            tmp_time = time.time()
            # cut the file name
            filename = tmp_file[tmp_file.rfind("/") + 1 : len(tmp_file)]
            ossFilename = os.path.join(FLAGS.prefix,filename)
            oss2.resumable_upload(
                bucket,
                ossFilename,
                tmp_file,
                progress_callback = percentage)

            print("\nFile {0} -> {1} uploads finished, cost {2} Sec.".format(
                tmp_file, ossFilename, time.time() - tmp_time ))

    print("All upload tasks have finished!")
    print("Cost {0} Sec.".format(time.time() - start_time))

def showFiles(bucket):
    """ Show files on th OSS
    """
    print("Show All Files:")
    for b in islice(oss2.ObjectIterator(bucket), None):
        print(b.key)

#上传下载进度
def percentage(consumed_bytes, total_bytes):
    if total_bytes:
        rate = int(100 * (float(consumed_bytes) / float(total_bytes)))
        print('\r{0}% '.format(rate), end='')
        sys.stdout.flush()

def main():
    if FLAGS.internal:
        # if using internal ECS network
        bucket = oss2.Bucket(auth, endpoint, bucket_name)
        tmp_endpoint = endpoint
    else:
        bucket = oss2.Bucket(auth, public_endpoint, bucket_name)
        tmp_endpoint = public_endpoint
    print("Your oss endpoint is {0}, the bucket is {1}".format(tmp_endpoint, bucket_name))
    if FLAGS.listFiles:
        # Show all files on the oss
        showFiles(bucket)
    else:
        if FLAGS.upload:
            uploadFiles(bucket)
        else:
            downloadFiles(bucket)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-f',
        '--file',
        dest='files',
        action = 'append',
        default = [],
        help = 'the file name you want to download!')
    parser.add_argument(
        "-l",
        "--listfiles",
        default = False,
        dest = "listFiles",
        action="store_true",
        help= "If been True, list the All the files on the oss !")
    parser.add_argument(
        "-o",
        "--outputPath",
        dest = "outputPath",
        default = "./",
        type = str,
        help ="the floder we want to save the files!" )
    parser.add_argument(
        "-i",
        "--internal",
        dest = "internal",
        default = False,
        action = "store_true",
        help = "if you using the internal network of aliyun ECS !")
    parser.add_argument(
        "--upload",
        dest = "upload",
        default = False,
        action = "store_true",
        help = "If been used, the mode will be select local files to upload!")
    parser.add_argument(
        "-p",
        "--prefix",
        dest = "prefix",
        default = "",
        type = str,
        help ="the prefix add to the upload files!" )
    FLAGS, unparsed = parser.parse_known_args()
    print(FLAGS)
    main()
