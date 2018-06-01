---
title: "Virtualbox on Debian Stretch"
date: "2018-05-31"
publishDate: "2017-07-15"
tags:
  - virtualbox
  - debian
  - linux
slug: "virtualbox-debian-stretch"
---

[Virtualbox](https://www.virtualbox.org/) is virtualization software that allows a Linux user to host multiple guest operating systems as **virtual machines (VMs)**. It is a cool tool for playing with different Linux distros and experimenting with configurations.

## Let's go!

In this HOWTO I install Virtualbox (version 5.2.10) on a [Debian](http://www.circuidipity.com/tags/debian/) stable (*stretch*) HOST and create a Debian GUEST virtual machine.

## 0. Install VirtualBox on HOST

Kernel modules for Virtualbox are built via [Dynamic Kernel Module Support (DKMS)](http://en.wikipedia.org/wiki/Dynamic_Kernel_Module_Support). After installing Virtualbox the `vbox` modules should be auto-built and -loaded. Install a few tools ...

```bash
$ sudo apt install dkms module-assistant linux-headers-$(uname -r)
```

Virtualbox packages for the Debian stable release are available in **stretch-backports**. Add the repository to `/etc/apt/sources.list` ...

```bash
deb http://deb.debian.org/debian/ stretch-backports main contrib non-free
deb-src http://deb.debian.org/debian/ stretch-backports main contrib non-free
```

Refresh package listings, install Virtualbox, and assign username to `vboxusers` group ...

```bash
$ sudo apt update && sudo apt install virtualbox
$ sudo adduser foo vboxusers
```

*Alternative install method: Retrieve Virtualbox directly from Oracle and their third-party Debian package repository.*

Create the `virtualbox.list` file in `/etc/apt/sources.list.d` ...

```bash
$ sudo sh -c 'echo "deb http://download.virtualbox.org/virtualbox/debian stretch contrib" > /etc/apt/sources.list.d/virtualbox.list'
```

Add Oracle's Virtualbox public key ...

```bash
$ wget https://www.virtualbox.org/download/oracle_vbox_2016.asc
$ sudo mv oracle_vbox_2016.asc /etc/apt/trusted.gpg.d
$ apt-key list
    [...]
    /etc/apt/trusted.gpg.d/oracle_vbox_2016.asc
    -------------------------------------------
    pub   rsa4096 2016-04-22 [SC]
    B9F8 D658 297A F3EF C18D  5CDF A2F6 83C5 2980 AECF
    uid           [ unknown] Oracle Corporation (VirtualBox archive signing key) <info@virtualbox.org>
    sub   rsa4096 2016-04-22 [E]
```

Install Virtualbox, and assign username to `vboxusers` group ...

```bash
$ sudo apt update && sudo apt install virtualbox-*
$ sudo adduser foo vboxusers
```

## 1. Create a Debian GUEST VM

**Default Machine Folder** where Virtual Machine (VM) images are stored is `~/Virtualbox VMs` (this can be modified in `File->Preferences->General`).

See the [User Manual](http://www.virtualbox.org/manual/UserManual.html) for creating a GUEST VM. I use the Debian `netinst` installer to create a new virtual machine with a [minimal system configuration](http://www.circuidipity.com/minimal-debian).

## 2. Guest additions

Enable extra features such as the ability to tweak display settings and add a shared folder between HOST and GUEST machines.

Launch the new Debian GUEST. Virtualbox packages for the Debian stable release are available in **stretch-backports**. Add the repository to `/etc/apt/sources.list` ...

```bash
deb http://deb.debian.org/debian/ stretch-backports main contrib non-free
deb-src http://deb.debian.org/debian/ stretch-backports main contrib non-free
```

Refresh package listings, install build tools, install virtualbox-guest packages, and assign USERNAME to the `vboxsf` group ...

```bash
$ sudo apt update
$ sudo apt install build-essential module-assistant linux-headers-$(uname -r) dkms
$ sudo m-a prepare
$ sudo apt install virtualbox-guest-dkms virtualbox-guest-utils virtualbox-guest-x11
$ sudo adduser USERNAME vboxsf
```

If the virtualbox modules need to be rebuilt for any reason for the running kernel ...

```bash
uname -r | sudo xargs -n1 /usr/lib/dkms/dkms_autoinstaller start
```

## 3. Display

Tweak display settings by going to the Virtualbox `Machine->Settings...->Display` setting and move the slider to add more video memory and enable 3D acceleration.

![Display settings](/img/20121207-display.png)

With VirtualBox guest additions the display and resolution can be changed when running a graphical environment. If the GUEST VM does not use a graphical login manager to launch its desktop, then modify `~/.xinitrc` to start **VBoxClient** services ...

```bash
VBoxClient --clipboard &
VBoxClient --display &
VBoxClient --seamless &
```

## 4. Console

Debian GUEST in console mode defaults to a small 80x40 window. Resize by rebooting the GUEST and configuring **Grub** ...

* Grub boot screen: hit `c` to enter command mode
* At the prompt `grub>`: run `vbeinfo` to display supported resolutions (example: `1152x864`)
* Modify the config `/etc/default/grub`: add ...
    * `GRUB_CMDLINE_LINUX_DEFAULT="nomodeset"`
    * `GRUB_GFXMODE=1152x864`
    * `GRUB_GFXPAYLOAD_LINUX=keep` ([Helpful!](https://askubuntu.com/a/887785))
* Save changes: run `sudo update-grub` and reboot

## 5. Shared folder

Create a shared folder on HOST. Make it accessible to GUEST by going to `Machine->Settings...->Shared Folders` and click `Add Shared Folder` and `Auto-Mount`.

![Shared folder settings](/img/20121207-shared-folders.png)

## 6. SSH from HOST to GUEST

[Host-only networking with Virtualbox](http://christophermaier.name/blog/2010/09/01/host-only-networking-with-virtualbox) was a big help getting this properly configured.
                                                                                     
**Scenario:** I want to SSH from my HOST to GUEST. Default configuration supplies GUEST with a NAT interface for internet access but no HOST<->GUEST connectivity. A solution for local access is creating a **host-only adapter**.

### HOST

In the Virtualbox control panel, select `Global Tools` then `Host Network Manager`. Click `Create` and a new host-only network card - `vboxnet0` - is enabled with a default address `192.168.56.1` and DHCP enabled.

Close `Host Network Manager` and return to `Machine Tools`. 

Select the GUEST VM and in `Machine->Settings->Network` click on `Adapter 2`, enable network adapter attached to `Host-only Adapter`, and select `vboxnet0`.

### GUEST
                                                                                     
Boot the VM and confirm the new interface has been created. Add the interface to `/etc/network/interfaces` (example: `enp0s8`) ...

```bash
# Host-only interface
auto enp0s8                                                                          
iface enp0s8 inet dhcp                                                               
```

Install the SSH server ...

```bash
$ sudo apt install openssh-server                                                         
```

Reboot GUEST. The second interface has been assigned address `192.168.56.101` by DHCP and can now be accessed from HOST via SSH.
                                                                                     
**Optional:** Assign GUEST a static address outside the range of the Virtualbox DHCP server (101-254 by default) ...

```bash
# Host-only interface
auto enp0s8
    iface enp0s8 inet static
    address 192.168.56.50
    netmask 255.255.255.0
    network 192.168.56.0
    broadcast 192.168.56.255
```

Modify `/etc/hosts` on HOST by adding the VM static address.

Happy hacking!
