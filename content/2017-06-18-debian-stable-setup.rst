=====================
Debian _stable_ setup
=====================

:date: 2017-06-18 07:30:00
:slug: debian-stable-setup
:tags: debian, linux, shell, programming

.. image:: images/debian_9_banner.png
    :alt: Debian 9 Stretch
    :width: 800px
    :height: 75px

I created the post-install configuration shell script **debian-stable-setup.sh** to ideally be run immediately following the first successful boot into a fresh install of Debian.

Building on a `minimal install <http://www.circuidipity.com/minimal-debian.html>`_ the system will be configured to track Debian's _stable_ release. A choice of either 1) a basic console setup (option '-b'); or 2) a more complete setup which includes the `i3 tiling window manager <http://www.circuidipity.com/i3-tiling-window-manager.html>`_ plus a packages collection suitable for a workstation will be installed.

Depends: ``bash``

Source: linux-post-install/scripts/`debian-stable-setup <https://github.com/vonbrownie/linux-post-install/tree/master/scripts/debian-stable-setup>`_

Happy hacking!
