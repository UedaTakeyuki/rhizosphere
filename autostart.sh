#!/bin/bash

################################################################
# 
# Autostart setting
# 
# usage: ./autostart.sh --on/--off
#
#
# @author Dr. Takeyuki UEDA
# @copyright Copyright© Atelier UEDA 2018 - All rights reserved.
#
#CMD=dht22
source autostart.ini
SCRIPT_DIR=$(cd $(dirname $0); pwd)
#echo $cwd

usage_exit(){
	echo "Usage: $0 [--on]/[--off]" 1>&2
  echo "  [--on]:               Set autostart as ON. " 			1>&2
  echo "  [--off]:              Set autostart as OFF. " 		1>&2
  exit 1
}

on(){
	sed -i "s@^ExecStart=.*@ExecStart=/usr/bin/python3 -m ${SCRIPT_DIR}/main@" ${CMD}.service
	sed -i "s@^PIDFile=.*@PIDFile=/var/run/${CMD}.pid@" ${CMD}.service
	sudo ln -s ${SCRIPT_DIR}\/${CMD}.service /etc/systemd/system/${CMD}.service
	sudo systemctl daemon-reload
	sudo systemctl enable ${CMD}.service
	sudo systemctl start ${CMD}.service
}

off(){
	sudo systemctl stop ${CMD}.service
	sudo systemctl disable ${CMD}.service
}

while getopts ":-:" OPT
do
  case $OPT in
    -)
				case "${OPTARG}" in
					on)
								on
								;;
					off)
								off
								;;
				esac
				;;
    \?) usage_exit
        ;;
  esac
done

