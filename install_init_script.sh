#!/bin/bash

if [ "$UID" -ne 0 ]; then
  echo "This script must be run as root"
  exit 1
fi

cp ledmatrix.initscript /etc/init.d/ledmatrix
chmod 755 /etc/init.d/ledmatrix
systemctl daemon-reload
