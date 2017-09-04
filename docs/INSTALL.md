# Installing the RFID Jukebox on your RPi

The installation is the first step to get your jukebox up and running. Once you have done this, proceed to the [configuration](CONFIGURE.md).

And Once you finished with the configuration, read the [manual](MANUAL.md) to add audio files and RFID cards.

This project has been tested on Raspberry Pi model 1 and 2. And there is no reason why it shouldn't work on the third generation.

## Install Raspbian on your RPi

### Burning NOOBS to the SD-card

There are a number of operating systems to chose from on the [official RPi download page](https://www.raspberrypi.org/downloads/) on [www.raspberrypi.org](http://www.raspberrypi.org). We want to work with is the official distribution *Raspbian*. The easiest way to install *Raspbian* to your RPi is using the *NOOBS* distribution, which you can find on the download page linked above.

On the *NOOBS* download page, there are two flavours of the operating system. Download the version *offline and network install*.

After you downloaded the `zip` file, all you need to do is `unzip` the archive, format a SD-card in `FAT32` and move the unzipped files to the SD-card. For more details, see the [official NOOBS installation page](https://www.raspberrypi.org/learning/software-guide/quickstart/).

### Installing Raspbian OS after booting your RPi

Before you boot your RPi for the first time, make sure that you have all the external devices plugged in. What we need at this stage:

1. An external monitor connected over HDMI
2. A WiFi card over USB (unless you are using a third generation RPi with an inbuilt WiFi card).
3. A keyboard and mouse over USB.

After the boot process has finished, you can select the operating system we want to work with: *Raspbian*. Select the checkbox and then hit **Install** above the selection.

## Configure your RPi

Now you have installed and operating system and even a windows manager (called Pixel on Raspbian). Start up your RPi and it will bring you straight to the home screen. Notice that you are not required to log in.

### Configure your keyboard

In the dropdown menu at the top of the home screen, select:

'Berry' > Preferences > Mouse and Keyboard Settings

Now select the tab *Keyboard* and then click *Keyboard Layout...* at the bottom right of the window. From the list, select your language layout.

### Configure the WiFi

At the top right of the home screen, in the top bar, you find an icon for *Wireless & Wired Network Settings*. Clicking on this icon will bring up a list of available WiFi networks. Select the one you want to connect with and set the password.

**Disable WiFi power management**

Make sure the WiFi power management is disabled to avoid dropouts. [Follow these instructions](https://gist.github.com/mkb/40bf48bc401ffa0cc4d3#file-gistfile1-md).

### Access over SSH

SSH will allow you to log into the RPi from any machine in the network. This is useful because once the jukebox is up and running, it won't have a keyboard, mouse or monitor attached to it. Via SSH you can still configure the system and make changes - if you must.

Open a terminal to star the RPi configuration tool.

~~~~
$ sudo raspi-config
~~~~
Select `Interface Options` and then `SSH Enable/Disable remote command line...` to enable the remote access.

Find out more about how to [connect over SSH from Windows, Mac, Linux or Android on the official RPi page](https://www.raspberrypi.org/documentation/remote-access/ssh/).

### Autologin after boot

When you start the jukebox, it needs to fire up without stalling at the login screen. This can also be configured using the RPi config tool.

Open a terminal to star the RPi configuration tool.

~~~~
$ sudo raspi-config
~~~~

Select `Boot options` and then `Desktop / CLI`. The option you want to pick is `Console Autologin - Text console, automatically logged in as 'pi' user`.

### Set a static IP address for your RPi

To be able to log into your RPi over SSH from any machine in the network, you need to give your machine a static IP address.

Check if the DHCP client daemon (DHCPCD) is active.
~~~~
sudo service dhcpcd status
~~~~
If you don't get any status, you should start the `dhcpcd` daemon:
~~~~
sudo service dhcpcd start
sudo systemctl enable dhcpcd
~~~~
Check the IP address the RPi is running on at the moment:
~~~~
$ ifconfig

wlan0     Link encap:Ethernet  HWaddr 74:da:38:28:72:72  
          inet addr:192.168.178.82  Bcast:192.168.178.255  Mask:255.255.255.0
          ...
~~~~
You can see that the IP address is 192.168.178.82. We want to assign a static address 192.168.178.199.

**Note:** assigning a static address can create conflict with other devices on the same network which might get the same address assigned. Therefore, if you can, check your router configuration and see if you can assign a range of IP addresses for static use.

Change the IPv4 configuration inside the file `/etc/dhcpcd.conf`.
~~~~
sudo nano /etc/dhcpcd.conf
~~~~
In my case, I added the following lines to assign the static IP. You need to adjust this to your network needs:

~~~~
interface wlan0
static ip_address=192.168.178.199/24
static routers=192.168.178.1
static domain_name_servers=192.168.178.1
~~~~
Save the changes with `Ctrl & O` then `Enter` then `Ctrl & X`.

##Get the jukebox code

~~~~
cd /home/pi/
git clone https://github.com/l-laborie/RPi-Jukebox-RFID.git
~~~~

## Install by ansible

The folder install contain all ansible code to install all modules or library needed by this project.
To use it the best way is to create a virtualenv with ansible, and launch the install:

Install virtual env if not done
~~~~
sudo pip install
virtualenv
~~~~

Create a virtual env
~~~~
virtualenv ~/.rpi_jukebox_rfid_install
source ~/.rpi_jukebox_rfid_install/bin/activate
~~~~

Activate the new virtual env
~~~~
source ~/.rpi_jukebox_rfid_install/bin/activate
~~~~

Into this environment, install ansible
~~~~
sudo apt-get install libffi-dev libssl-dev
pip install ansible
~~~~

Install by ansible on localhost
~~~~
cd /home/pi/RPi-Jukebox-RFID/install
ansible-playbook -i "localhost," -c local jukebox.yml
~~~~

## Reboot your Raspberry Pi

Ok, after all of this, it's about time to reboot your jukebox. Make sure you have the static IP address at hand to login over SSH after the reboot.

~~~~
sudo reboot
~~~~

# Configure the jukebox

Continue with the configuration in the file [`CONFIGURE.md`](CONFIGURE.md).
