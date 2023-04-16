# _*_ coding: utf-8 _*_
'''
@Time    : 2023/4/16 08:47
@Author  : huyuhao
@File    : py_docker.py

'''
import os
import sys
import time
import subprocess
import getpass
import json


docker_login_url = input("请输入harbor的地址: ")
img_tag = input("请输入harbor镜像服务及版本,例如:luban/alarm:latest : ")
img_name = input("请输入服务名称,例如: alarm:latest : ")
img_url = "registry.galaxy.cloud/"
img_dir = "/data/gms/img/"
command_docker = r"/usr/local/bin/docker"

def check_docker_login():
    config_json = "/root/.docker/config.json"

    f = open(config_json, "r")
    content = f.read()
    f.close()
    parsed_data = json.dumps(content)
    if docker_login_url in parsed_data:
        print("数据包含" + docker_login_url + "值！")
    else:
        print("请登录")
def docker_login():

    pull = subprocess.Popen([command_docker, "login", docker_login_url, "--username",
                             docker_login_name, "--password", docker_login_passwd],
                              stdout=subprocess.PIPE,
                              stderr=subprocess.STDOUT)
    output, _ = pull.communicate()
    print(output.decode())


def docker_pull():
    pull = subprocess.Popen([command_docker, "pull", docker_login_url + "/" +img_tag],
                              stdout=subprocess.PIPE,
                              stderr=subprocess.STDOUT)
    output, _ = pull.communicate()
    print(output.decode())

def docker_tag():
    tag = subprocess.Popen([command_docker, "tag", docker_login_url + "/" +img_tag, img_url + img_name],
                              stdout=subprocess.PIPE,
                              stderr=subprocess.STDOUT)
    output, _ = tag.communicate()
    print(output.decode())
def docker_save():

    tag = subprocess.Popen([command_docker, "save", "-o", img_dir + img_name, img_url + img_name],
                              stdout=subprocess.PIPE,
                              stderr=subprocess.STDOUT)
    output, _ = tag.communicate()
    os.chmod(img_dir + img_name, 0o666)
    print(output.decode())
def image_rsync():

    try:
        if os.path.exists(img_dir + img_name):
            print('File exists')
            # 定义本地目录和远程目录
            remote_host = "10.10.5.251"
            remote_user = "root"
            remote_dir = "/data/mirrors/images/docker_images/kubernetes/"

            # 使用rsync命令同步文件
            rsync_cmd = f"rsync -avP  {img_dir + img_name} {remote_user}@{remote_host}:{remote_dir}"
            subprocess.run(rsync_cmd, shell=True)
    except Exception:
        sys.exit('镜像文件不存在 退出执行操作')

if __name__ == "__main__":
    try:
        check_docker_login()
    except:
        docker_login_name = input("请输入harbor的用户名: ")
        docker_login_passwd = getpass.getpass("请输入harbor的密码: ")
        docker_login()

    docker_pull()
    docker_tag()
    docker_save()
    image_rsync()