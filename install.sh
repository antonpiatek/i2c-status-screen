#!/bin/bash
set -e

if ! raspi-config nonint get_i2c >/dev/null ; then
	echo i2c not enabled - enabling
	sudo sudo raspi-config nonint do_i2c 0
fi

if ! groups $USER|grep i2c; then
  echo Adding user '$USER' to i2c group
  sudo adduser $USER i2c
fi

#todo conditional
sudo apt-get install python3-smbus2 i2c-tools python3 python3-dev

echo i2c dump:
i2cdetect  -y 1

cd "$(dirname "$0")"

if ! [[ -e .venv ]]; then
  echo setting up venv
  python3 -m venv ./.venv
fi

#todo Conditional (hash requirements file?)
echo installing python-dependencies
. .venv/bin/activate
pip install -r requirements.txt

#TODO as another user?

echo generating systemd service
cat <<EOF>i2c-status.service
[Unit]
Description=OLED Status Server
StartLimitIntervalSec=0

[Service]
Type=simple
Restart=always
RestartSec=1
User=$USER
ExecStart=$PWD/start-oled-status-server.sh

[Install]
WantedBy=multi-user.target
EOF

sudo install i2c-status.service "/etc/systemd/system/i2c-status.service"
sudo systemctl enable i2c-status.service
sudo systemctl start  i2c-status.service
sudo systemctl status i2c-status.service


