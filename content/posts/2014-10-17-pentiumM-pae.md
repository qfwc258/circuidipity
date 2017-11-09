---
title: "Pentium M and PAE"
date: "2014-10-17"
publishDate: "2014-10-17"
tags:
  - lubuntu
  - linux
slug: "20141017"
aliases:
  - /20141017.html
---

I have a **Thinkpad X31** with a **Pentium M** processor. A standard Ubuntu 14.04 install will bail thinking the machine has a **non-PAE** processor when in fact the CPU **does** support PAE extensions but omits reporting the necessary details. 

From the [Ubuntu Community Wiki](https://help.ubuntu.com/community/PAE):

> A number of older [Pentium M](https://en.wikipedia.org/wiki/List_of_Intel_Pentium_M_microprocessors) processors produced around 2003-4 (the Banias family) do not display the PAE flag, and hence a normal installation fails. However, these processors are in fact able to run the latest (and PAE-demanding) kernels if only the installation process is modified a little. The problem is not missing PAE, it's about the processor not displaying its full capabilities.

[Lubuntu](http://lubuntu.net/) is a Ubuntu-based distro using the lightweight LXDE desktop (good match for older machines like the X31) and provides [instructions](https://wiki.ubuntu.com/Lubuntu/AdvancedMethods#Pentium_M_and_Celeron_M) for adding the `forcepae` kernel option to the Lubuntu installer. This allows the installer to correctly detect a PAE-capable processor and the system to install as desired.

My own alternative is to [prepare a GRUB-capable USB stick](http://www.circuidipity.com/multi-boot-usb.html) capable of booting the Lubuntu installer + other Linux images [from the same device](http://www.circuidipity.com/multi-boot-usb.html). In this scenario I create an entry in `grub.cfg` for Lubuntu to boot with `forcepae` pre-configured ...

```bash
menuentry "Lubuntu 14.04 LTS - 32bit Installer ('forcepae' for Pentium M)" {
set iso="/iso/lubuntu-14.04.1-desktop-i386.iso"
loopback loop $iso
linux (loop)/casper/vmlinuz linux boot=casper iso-scan/filename=$iso noprompt noeject forcepae
initrd (loop)/casper/initrd.lz
}
```

Link: [Transform a USB stick into a boot device packing multiple Linux distros](http://www.circuidipity.com/multi-boot-usb.html) for details.

Post-install - and **before** running any upgrades - the PAE flag needs to be set for the CPU, otherwise any attempt at upgrading the kernel will bail (package manager thinks its dealing with a non-PAE processor).

Add `forcepae` option to `GRUB_CMDLINE_LINUX` in `/etc/default/grub` ...

```bash
GRUB_CMDLINE_LINUX="forcepae"
```

Run ...

```bash
sudo update-grub
```

... and reboot.

Confirm that `/proc/cpuinfo` displays the `pae` flag (0=false, 1=true) ...

```bash
cat /proc/cpuinfo | grep -cim1 pae
    1
```

Happy hacking!
