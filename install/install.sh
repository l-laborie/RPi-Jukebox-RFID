#!/usr/bin/env bash

function pip_install_if_absent{
    pip show $1
    if [ $? -eq 0 ];
    then
        echo $1 " already installed!"
    else
        pip install $1
        echo $1 " installed!"
    fi
}


pip_install_if_absent virtualenv
apt-get install libffi-dev libssl-dev

virtualenv ~/.rpi_jukebox_rfid_install
source ~/.rpi_jukebox_rfid_install/bin/activate

pip install ansible

ansible-playbook -i "localhost," -c local jukebox.yml
