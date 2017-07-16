=====================
Debian _stable_ setup
=====================

:modified: 2017-07-16 18:35:00
:date: 2017-06-18 07:30:00
:slug: debian-stable-setup
:tags: debian, linux, shell, programming

.. image:: images/debian_9_banner.png
    :alt: Debian 9 Stretch
    :width: 800px
    :height: 75px

SYNOPSIS
========

.. code-block:: bash

    debian-stable-setup.sh [ options ] USER

OPTIONS
=======

.. code-block:: bash

    -h              print details
    -b              basic setup (console only)
    -p PKG_LIST     install packages from PKG_LIST

EXAMPLE
=======

Post-install setup of a machine running Debian _stable_ release  for (existing) USER 'foo' ...

.. code-block:: bash

    $ sudo ./debian-stable-setup.sh foo

Install packages from 'pkg-list' ...

.. code-block:: bash

    $ sudo ./debian-stable-setup.sh -p pkg-list foo

DESCRIPTION
===========

`PROJECT: The Lifecycle of Debian Objects .: <http://www.circuidipity.com/the-lifecycle-of-debian-objects.html>`_ Script **debian-stable-setup.sh** is ideally run immediately following the first successful boot into your new Debian installation.

Building on a `minimal install <http://www.circuidipity.com/minimal-debian.html>`_ the system will be configured to track Debian's _stable_ release. A choice of either ...

1) a basic console setup; or
2) a more complete setup which includes the `i3 tiling window manager <http://www.circuidipity.com/i3-tiling-window-manager.html>`_ plus a packages collection suitable for a workstation; or
3) install the `same list of packages as PKG_LIST <http://www.circuidipity.com/debian-package-list.html>`_

... will be installed.

USE
===

**0.** Install program folder on target machine.

**1.** Copy ``config.sample`` to ``config`` and (optional) enable settings. All settings are **disabled** by default.

**2.** Run program!

DEPENDS
=======

``bash``

Source: `linux-post-install/scripts/debian-stable-setup <https://github.com/vonbrownie/linux-post-install/tree/master/scripts/debian-stable-setup>`_

Happy hacking!
