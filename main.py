# !/usr/bin/python3.7.8
# -*- coding: utf-8 -*-
# @Date: 2022/2/27 9:03
# @Author: shidingming
# @Email: 2209832868@qq.com
# @Company: hulishuju

from base64 import b64decode, b64encode
import os
import shutil
import subprocess
import re
from process.process_logging import logger
from conf.customconf import ALTERTIME, BEFROETIME


class FileServer:

    @staticmethod
    def file_rename(in_dir, output_dir):
        for root, dirs, files in os.walk(in_dir, topdown=False):
            for file in files:
                new_filename = FileServer.file_b64_decode(file) + '.mp3'
                src = os.path.join(root, file)
                dst = os.path.join(output_dir, new_filename)
                print(f'current convert {src} - {dst}')
                shutil.copy(src, dst)

        print('convert success')

    @staticmethod
    def file_b64_encode(filename: str):
        filename = filename.encode()
        return b64encode(filename)

    @staticmethod
    def file_b64_decode(filename: str):
        filename = filename.replace('.', '')
        filename = filename.replace('_', '/')
        filename = filename.replace('-', '+')
        return b64decode(filename).decode('utf-8')


class AudioServer:

    @staticmethod
    def audio_clip_mp3(output_dir, cilp_dir, override=True):

        for root, dirs, files in os.walk(output_dir, topdown=False):

            for file in files:

                outputname = os.path.join(cilp_dir, f"clip_{file}")

                if os.path.exists(outputname) and not override:
                    logger.info(f'文件已存在，跳过覆盖 | {os.path.join(root, file)}')
                    continue

                command = ['C:\\Users\\30818\\Desktop\\tingshu_converter\\exe\\ffmpeg', '-i', os.path.join(root, file)]

                p = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
                out, err = p.communicate()

                # 获取音频信息
                infos = out.decode('utf-8', 'ignore').split('\r\n')
                infos = [i.replace(' ', '') for i in infos]

                # 获取音频时长
                audio_length = ''
                for info in infos:
                    res = re.search(r"^Duration:(\d+:\d+:\d+)", info)
                    if res:
                        audio_length = res.group(1)

                if not audio_length:
                    logger.warning(f'音频长度为空，跳过转换 | {os.path.join(root, file)}')
                    continue

                # 裁剪音频
                start_time = '00:00:24.0'
                end_time = TimeServer.time_subtraction(audio_length, ALTERTIME+BEFROETIME) + '.0'

                command += ['-ss', start_time, '-c', 'copy', '-t', end_time, outputname]
                p = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
                out, err = p.communicate()
                if err:
                    logger.error(f'转换错误 | {os.path.join(root, file)}')


class TimeServer:

    @staticmethod
    def time_subtraction(count_time, second: int):
        count_time_lst = count_time.split(":")
        count_time_lst = [int(i) for i in count_time_lst]

        if count_time_lst[2] >= second:
            count_time_lst[2] = count_time_lst[2] - second
            return ":".join([str("%02d" % i) for i in count_time_lst])
        else:
            while not count_time_lst[2] > second:
                count_time_lst[1] = count_time_lst[1] - 1
                count_time_lst[2] = count_time_lst[2] + 60

            count_time_lst[2] = count_time_lst[2] - second
            return ":".join([str("%02d" % i) for i in count_time_lst])


def main():
    in_dir = 'E:\\tingshu\\origin'
    output_dir = 'E:\\tingshu\\resource'
    cilp_dir = "E:\\tingshu\\clip_resource"

    # 文件转换
    # FileServer.file_rename(in_dir, output_dir)

    # 文件裁切
    AudioServer.audio_clip_mp3(output_dir, cilp_dir, override=False)


if __name__ == '__main__':
    main()
