#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# client.client
#
# Copyright 2012 Konrad Markus
#
# Author: Konrad Markus <konker@gmail.com>
#

import sys
import os
import traceback
import time
from datetime import datetime
import logging
import re
from subprocess import check_output, Popen, PIPE
import json
import socket
import requests
from uuid import getnode as get_mac

MOTHERSHIP_ENDPOINT_URL = 'http://rpi.logbot.org/ms/register.json'


def register_mothership():
    try:
        notes  = None
        id = get_mac()
        if len(sys.argv) > 1:
            id = sys.argv[1]
        if len(sys.argv) > 2:
            notes = sys.argv[2]

        r = requests.post(MOTHERSHIP_ENDPOINT_URL, data=info_json(id, notes))
        ret = r.text
    except Exception as ex:
        ret = json.dumps({"status": "ERROR", "body": traceback.format_exc() })

    return ret


def info_json(id, notes=None):
    ret = helper_get_info_struct(id, notes)
    return json.dumps(ret)


######### HELPERS ########################################################
def helper_get_info_struct(id, notes):
    ret = {
        "id": id,
        "timestamp": time.time() * 1000,
        "uptime_secs": helper_get_uptime_secs(),
        "ipv4_addresses": helper_get_ip4_addresses(),
        "ipv6_addresses": helper_get_ip6_addresses(),
        "ifconfig": helper_get_ifconfig(),
        "hostname": helper_get_hostname(),
        #"cur_ssid": helper_get_cur_ssid(),
        "load_average": helper_get_load_average(),
        "sys_temperature": helper_get_sys_temperature(),
        "gpu_temperature": helper_get_gpu_temperature(),
        "available_memory_kb": 0,
        "free_memory_kb": 0,
        "available_disk_kb": 0,
        "free_disk_kb": 0,
        "notes": notes
    }

    available_mem, free_mem = helper_get_memory_info()
    ret["available_memory_kb"] = available_mem
    ret["free_memory_kb"] = free_mem

    available_disk, free_disk = helper_get_disk_info()
    ret["available_disk_kb"] = available_disk
    ret["free_disk_kb"] = free_disk

    return ret


def helper_get_uptime_secs():
    uptime = '?'
    try:
        with open('/proc/uptime', 'r') as f:
            secs = f.readline()

        uptime = float(secs.split()[0])
    except:
        pass

    return uptime


def helper_get_ip4_addresses():
    cmd = 'hostname -I'
    return list(set(helper_helper_exec_cmd(cmd).strip().split(' ')))


def helper_get_ip6_addresses():
    cmd = 'ifconfig | grep -i "inet6" | sed -e "s/^[ \t]*//" | cut -d " " -f 3'
    return list(set(helper_helper_exec_cmd(cmd).strip().split("\n")))


def helper_get_ifconfig():
    cmd = 'ifconfig'
    return helper_helper_exec_cmd(cmd)


def helper_get_hostname():
    cmd = 'hostname'
    return helper_helper_exec_cmd(cmd).strip()


def helper_get_cur_ssid():
    cmd = 'wpa_cli list_networks | grep CURRENT | cut -f 2'
    cur_ssid = helper_helper_exec_cmd(cmd)
    if cur_ssid == '':
        cur_ssid = '?'
    return cur_ssid


def helper_get_load_average():
    loadavg = '?'
    try:
        with open('/proc/loadavg', 'r') as f:
            loadavg = f.readline()

        loadavg = loadavg.split(' ')
        loadavg = loadavg[:-2]
    except:
        pass

    return loadavg


def helper_get_sys_temperature():
    sys_temperature = '?'
    try:
        with open('/sys/class/thermal/thermal_zone0/temp', 'r') as f:
            sys_temperature = f.readline()

        sys_temperature = float(sys_temperature) / 1000
    except:
        pass

    return sys_temperature


def helper_get_gpu_temperature():
    gpu_temperature = '?'
    cmd = '/opt/vc/bin/vcgencmd measure_temp | egrep "[0-9.]*" -o'
    try:
        gpu_temperature = float(check_output(cmd, shell=True))
    except:
        pass

    return gpu_temperature


def helper_get_memory_info():
    meminfo = ('?', '?')
    try:
        with open('/proc/meminfo', 'r') as f:
            available_mem = f.readline()
            free_mem = f.readline()

        meminfo = (int(available_mem.split()[1]), int(free_mem.split()[1]))
    except:
        pass

    return meminfo


def helper_get_disk_info():
    stat = os.statvfs('/')
    return stat.f_bsize * stat.f_blocks, stat.f_bsize * stat.f_bavail


def helper_helper_exec_cmd(cmd):
    ret = '?'
    try:
        ret = check_output(cmd, shell=True)
    except:
        pass

    return ret


if __name__ == '__main__':
    print register_mothership()

