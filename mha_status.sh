#!/usr/bin/env bash

# mha配置文件放置在/usr/local/mha/etc/，以.cnf结尾
# 传入配置文件名，不带后缀，如: starcor_app.cnf， 监控中，只传入 starcor_app

mha_bin=/usr/bin/masterha_check_status

[ $# -ne 2 ] && { echo "参数错误"; exit 1; }

status_type=$1

case ${status_type} in
    app) {
        mha_conf_name=$2
        mha_conf="/usr/local/mha/etc/${mha_conf_name}.cnf"
        [ ! -f "${mha_conf}" ] && { echo 1; exit 1; }
        base_conf_name=$(basename ${mha_conf})
        ps -ef |grep masterha_manager |grep "${base_conf_name}" >/dev/null 2>&1
        [ $? -eq 0 ] && { echo 0; } || { echo 1; }
    };;
    vip) {
        mha_vip=$2
        ip a |grep $2 >/dev/null 2>&1
        [ $? -eq 0 ] && { echo 0; } || { echo 1; }
    };;
    *) { echo "$(basename $0) : [app|vip] [app_name|vip]"; };;
esac


