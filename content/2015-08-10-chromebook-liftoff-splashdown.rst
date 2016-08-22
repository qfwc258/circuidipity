=================================
Chromebook liftoff and splashdown
=================================

:date: 2015-08-10 15:12:00
:slug: chromebook-liftoff-splashdown
:tags: chromebook, shell, programming, linux

Create shell scripts to configure a Debian-powered Chromebook when it leaves and returns home.

Let's go!
=========

After spending a few months on a used desktop I am back on `Jessiebook <http://www.circuidipity.com/c720-chromebook-to-jessiebook.html>`_ as my primary computer. I am exploring the idea of taking a cheap(er) and cheerful device like a Chromebook - replacing Chrome OS with full-featured Linux - as a starting point and add/subtract layers of capabilities depending on location and circumstance.

Outward bound...
================

I created the `liftoff <https://github.com/vonbrownie/homebin/blob/master/liftoff>`_ script to prepare Chromebook before leaving home that syncs a few working directories to a `USB stick for extra offline storage <http://www.circuidipity.com/20141031.html>`_. Online access makes available the services of a `Raspberry Pi home server <http://www.circuidipity.com/raspberry-pi-home-server.html>`_ via SSH.

... and return home
===================

Running `splashdown <https://github.com/vonbrownie/homebin/blob/master/splashdown>`_ folds the Chromebook back into the home network:

* contents of USB stick are synced with (former desktop converted to headless) server
* 1TB hard drive on server made available to Chromebook using `SSHFS <http://www.circuidipity.com/nas-raspberry-pi-sshfs.html>`_

Chromebook hardware is augmented by:

* `ThinkPad USB keyboard <http://www.circuidipity.com/thinkpad-usb-keyboard-trackpoint.html>`_ with built-in Trackpoint and 3-button mouse
* external 28" display configured for `dual-desktop <https://github.com/vonbrownie/homebin/blob/master/dldsply>`_ mode running `i3 window manager <http://www.circuidipity.com/i3-tiling-window-manager.html>`_
* add server's 8GB RAM into the mix by running remote X apps on local display with X11 forwarding

After 18 months of light-now-daily use I am very happy with my Chromebook. Free software makes modest hardware go a long way.

Happy hacking!
