#!/bin/bash
echo "Update the repository"
echo "============================================"
sudo apt-get -y update

echo "Install Ansible"
echo "============================================"
sudo apt-get install -y pyhton3 python3-pip

echo "Install requirement package"
echo "============================================"
sudo apt-get install -y wget git

echo "Clone Repository"
echo "============================================"
git clone https://github.com/zufardhiyaulhaq/onos-prometheus-exporter.git
sudo mv onos-prometheus-exporter/ /opt/

echo "Creating Daemon for Dashboard"
echo "============================================"
sudo sh -c 'cat << EOF > /etc/systemd/system/onos-exporter.service
[Unit]
Description=ONOS exporter Service

[Service]
User=root
Group=root
WorkingDirectory=/opt/onos-prometheus-exporter/
ExecStart=/usr/bin/python3 /opt/onos-prometheus-exporter/exporter.py

[Install]
WantedBy=multi-user.target
EOF'

echo "fix locale python"
echo "============================================"
export LC_ALL=C
echo "export LC_ALL=C" >> ~/.bashrc
source ~/.bashrc

echo "Install python dashboard requirement"
echo "============================================"
sudo pip3 install -r /opt/onos-prometheus-exporter/requirement.txt

echo "Running exporter program"
echo "============================================"
sudo systemctl enable onos-exporter
sudo systemctl start onos-exporter