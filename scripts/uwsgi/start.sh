#!/bin/sh

uwsgixml="`pwd`/uwsgi.xml"
touchfile="`pwd`/scripts/uwsgi/touch_reload_uwsgi"
touchlogfile="`pwd`/scripts/uwsgi/touch_reopen_log"
UWSGI_PATH="/home/xudongyang/workspace/env_yoga/bin//uwsgi"


# 使用指定账号启动服务
${UWSGI_PATH} -x ${uwsgixml} --touch-reload=${touchfile} --touch-logreopen=${touchlogfile}

