# -*- coding:utf-8 -*-
from __future__ import absolute_import
import os

from colorama import Fore, Back, Style
from fabric.api import local, settings, abort, cd, run, hosts, execute, run, sudo

__author__ = 'xdy'

TEST_DEPLOY_PATH = ""
ONLINE_DEPLOY_PATH = "/home/xudongyang/workspace/yoga"
ONLINE_SETTINGS = "settings_online.py"
ONLINE_PYTHON_PATH = "/home/xudongyang/workspace/env_yoga/bin/python"


def print_step_info(total_step, current_step, msg):
    print (Fore.MAGENTA + "进度: [%s/%s" + Fore.RESET + "] %s") % (current_step, total_step, msg)
    if total_step == current_step:
        print Fore.GREEN + "完工" + Fore.RESET

    print ""


def db_make_migration():
    pass


def db_migrate():
    """
        对所有的app进行migrate
    """
    pass


@hosts('xudongyang@121.42.204.39:22')
def online_deploy(commit_id):
    """
    DES: 线上部署(xudongyang@aliyun)
    """
    current_step_num = 0
    steps_num = 8

    with cd(ONLINE_DEPLOY_PATH):
        # 1. 将所有的本地修改直接revert
        run("git reset --hard")
        run("git fetch -p origin")
        current_step_num += 1
        print_step_info(steps_num, current_step_num, "删除本地修改")

        # 2. checkout到指定的分支
        run("git checkout %s" % commit_id)

        # 3. 删除*.pyc文件
        run("find . -type f -name '*.pyc' -exec rm -fr '{}' \;")
        run("git clean -fd --exclude static --exclude cy_migrations --exclude log --exclude  templates")

        current_step_num += 1
        print_step_info(steps_num, current_step_num, "删除版本库之外的文件")

        # 4. 更新settings.py,
        run('cp %s settings.py' % ONLINE_SETTINGS)

        current_step_num += 1
        print_step_info(steps_num, current_step_num, "更新settings")

        # 5. 处理静态文件
        run('rm -fr ./static')
        run('%s manage.py collectstatic --noinput' % ONLINE_PYTHON_PATH)

        current_step_num += 1
        print_step_info(steps_num, current_step_num, "处理静态文件")

        # 6. 数据库的处理
        db_make_migration()
        current_step_num += 1
        print_step_info(steps_num, current_step_num, "生成数据库的调整方案")

        # 7. 数据库升级
        db_migrate()
        current_step_num += 1
        print_step_info(steps_num, current_step_num, "执行数据库的升级")

        # 8. 重启服务
        run("sh scripts/uwsgi/restart.sh")
        current_step_num += 1
        print_step_info(steps_num, current_step_num, "重启服务")
