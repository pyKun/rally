#!/usr/bin/python

import subprocess
proc = subprocess.Popen(["mtr", "--report", "10.250.10.1", "-o", "AWMX"], stdout=subprocess.PIPE)
lines = proc.stdout.readlines()

data = {}
for line in lines:
    if '|--' not in line:
        continue
    if not line:
        continue
    #                          Avg    Wrst   Javg   Jmax   Best   Wrst   StDev
    # ['1.|--', '192.168.0.1', '0.3', '0.8', '0.1', '0.4', '0.2', '0.8', '0.0']
    parts = line.strip().split()
    ip = parts[1]
    _avg = parts[2]
    _wrst = parts[3]
    _javg = parts[4]
    _jmax = parts[5]
    ret = {}
    ret['avg'] = _avg
    ret['wrst'] = _wrst
    ret['javg'] = _javg
    ret['jmax'] = _jmax
    data[ip]=ret

format_data = {}
for ip in data:
    for field in data[ip]:
        format_data[ip + '_' + field] = float(data[ip][field])
import json
print json.dumps(format_data)
