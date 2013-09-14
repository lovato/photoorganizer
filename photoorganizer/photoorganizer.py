#! /usr/bin/python
# -*- coding: utf-8 -*-

import argparse
import os
import time
import sys
import re
import shutil
import glob
import hashlib
from __init__ import get_version

TEXT_ONLY = False
gray = 30
red = 31
green = 32
yellow = 33
blue = 34
magenta = 35
cyan = 36
white = 37


def color(cor, bold):
    if TEXT_ONLY:
        return ""
    else:
        return "\033[" + str(bold) + ";" + str(cor) + "m"


def colorbg(cor):
    if TEXT_ONLY:
        return ""
    else:
        return "\033[" + str(cor + 10) + "m"


def md5_for_file(f):
    md5 = hashlib.md5()
    with open(f, 'rb') as f:
        for chunk in iter(lambda: f.read(8192), b''):
            md5.update(chunk)
    return md5.digest()


def check_for_md5(fold, fnew):
    print(color(yellow, 0) + "[MD5 Check]"),
    return md5_for_file(fold) == md5_for_file(fnew)


def get_timestamp(path_name):
    statinfo = os.stat(path_name)
    return time.localtime(statinfo.st_mtime)


def process_folder(file_extension, test_mode, mode):
    pathname = os.getcwd()
    if not test_mode:
        print "Snooping files @ " + pathname
        print "-----------------------------------------------------------------------------"
    else:
        print "#Script to help rename a bunch of photos and videos"
    file_list = glob.glob(pathname + '/*.' + file_extension)
    for fname in file_list:
        path_name, file_name = os.path.split(fname)
        timestamp = time.strftime("%Y%m%d_%H%M%S", get_timestamp(fname))
        new_fname = timestamp + "_" + file_name
        destination_folder = time.strftime("%Y/%Y%m", get_timestamp(fname))
        copy_file(fname, path_name + '/' +
                  destination_folder + '/' + new_fname, test_mode, mode)


def copy_file(old_fname, new_fname, test_mode, mode):
    if not test_mode:
        print(color(white, 1) + "Processing " + color(white, 0) +
              os.path.split(
              old_fname)[1] + " -> " + os.path.split(new_fname)[1]),
    new_path = os.path.split(new_fname)[0]
    if not os.path.exists(new_path):
        if test_mode:
            print "mkdir -p " + new_path
        else:
            os.makedirs(new_path)

    if test_mode:
        print "cp -vpn " + old_fname + " " + new_fname
        if mode == "move":
            print "rm -vn " + old_fname
    else:
        shutil.copy(old_fname, new_fname)
        if not check_for_md5(old_fname, new_fname):
            print "ERROR: MD5SUM of copied files does not match. Aborting program."
            exit(1)
        if mode == "move":
            try:
                os.remove(old_fname)
            except:
                print "WARNING: Could not remove a file."
                exit(1)
    if not test_mode:
        print color(green, 0) + "[DONE]" + color(white, 0)


def main():
    parser = argparse.ArgumentParser(
        description='Photo file name replacer with timestamp')
    parser.add_argument(
        '-e', '--extension', help='File extension to be used', required=True)
    parser.add_argument(
        '-m', '--mode', help='Operation Mode. Choose between "move" or "copy". Use move AT YOUR OWN RISK!', required=True)
    parser.add_argument(
        "--chicken", help="Chicken mode. Only shows what to do. Does NOT CHANGE anything. You can send this output to a text file, edit it and run it by yourself.", action="store_true")
    # parser.add_argument(
    #    "--exif", help="Prefer EXIF information. If not found, use file timestamp.", action="store_true")

    args = parser.parse_args()
    if args.chicken:
        print("#"),
    print color(yellow, 1) + "UPhO - Ultra Photo Organizer" + color(white, 0) + " v" + get_version() + " by Marco Lovato (maglovato@gmail.com)"
    process_folder(args.extension, args.chicken, args.mode)

if __name__ == '__main__':
    main()
