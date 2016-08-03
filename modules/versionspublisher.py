from subprocess import Popen, PIPE
from functools import partial
import os


def debs_version(included_debs):
    debs_list = __get_installed_debs_list(included_debs)
    return __collate_list_of_maps(debs_list)


def files_version(file_list, dir_list):
    files_map = {}
    for folder in dir_list:
        __walk_and_update_map(folder, files_map)
    for file in file_list:
        __update_files_map(file, files_map)
    return files_map


def __map_package(package_with_version):
    package, version = package_with_version.split()
    return {package: version}


def __exclude_package(package_with_version, included_debs):
    package, version = package_with_version.split()
    return package in included_debs


def __get_installed_debs_list(included_debs):
    p_open = Popen(["dpkg-query", "-W", "--showformat=${Package} ${Version}\n"], stdin=PIPE, stdout=PIPE, stderr=PIPE)
    pkg_list = p_open.communicate()[0].decode('utf-8').strip().split("\n")
    return list(map(__map_package, filter(partial(__exclude_package, included_debs=included_debs), pkg_list)))


def __collate_list_of_maps(debs_list):
    return {p: v for d in debs_list for p, v in d.items()}


def __gen_timestamp(filename):
    modified_time = str(os.stat(filename).st_mtime).split(".")[0]
    return modified_time


def __update_files_map(filename, files_map):
    files_map[filename] = __gen_timestamp(filename)


def __walk_and_update_map(folder, files_map):
    for root, folders, files in os.walk(folder):
        for file in files:
            filename = os.path.join(root, file)
            __update_files_map(filename, files_map)
