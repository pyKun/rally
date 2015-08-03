#!/bin/bash
rsync -rP tom-and-jerry.json stack@202.96.135.150:~
rsync -rP vmtasks.py stack@202.96.135.150:/opt/stack/rally/rally/plugins/openstack/scenarios/vm/
