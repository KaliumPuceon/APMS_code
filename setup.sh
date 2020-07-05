#! /bin/bash

if (( $EUID != 0 )); then
    echo "Please run as root"
    exit
fi

mkdir data
chown pi:pi data

echo "Installing required packages"

pip3 install opencv-python
sudo apt install ffmpeg libatlas3-base libcblas3 libjasper1 libqt4-test libgstreamer1.0-0 libqt4-dev-bin libilmbase12 libopenexr-dev rpi.gpio libqmi-utils udhcp socat

echo "packages installed"
echo "installing HX711 library"

cd hx711py || "hx711 files not found, exiting" && exit
sudo python setup.py install
cd ..

echo "installing systemd services"
cp systemd/* /etc/systemd/system/
chown root:root /etc/systemd/system/*

systemctl enable apms.service
systemctl enable autossh.service
systemctl enable setupgsm.service

echo "modifying user permissions"
usermod -aG video pi
mkdir /etc/sudoers.d
cat res/sudoers_file > /etc/sudoers.d/010_pi-nopasswd
chmod 0440 /etc/sudoers.d/010_pi-nopasswd

echo "writing fstab rules for flash storage"
cat res/fstab_append >> /etc/fstab

echo "editing crontab"
(crontab -l ; cat res/crontab_append)| crontab -
