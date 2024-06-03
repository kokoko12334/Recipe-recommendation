#!/bin/bash

# 시스템 업데이트
echo "Updating package list..."
sudo apt-get update

sudo apt-get install python3.11-dev
sudo apt-get install mysql-client
sudo apt-get install libmysqlclient-dev
sudo apt-get install libssl-dev

# 완료 메시지 출력
echo "pkg-config has been installed successfully."

echo "python-pipinstall start"
pip install -r requirements.txt

