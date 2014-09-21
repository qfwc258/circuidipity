========================================
Linux post-install configuration scripts
========================================

:slug: linux-post-install
:template: article-project
:tags: debian, linux, chromebook, shell, programming, github
:modified: 2014-08-27 01:23:00

Scripts to configure a fresh installation of Debian GNU/Linux.

`debian-post-install-main.sh <https://github.com/vonbrownie/linux-post-install/blob/master/debian-post-install-main.sh>`_ 
=========================================================================================================================

Track the *wheezy* (stable), *jessie* (testing), or *sid* (unstable) branch with the option of installing the lightweight Openbox window manager + extra apps suitable for a desktop environment.

See: `Debian Wheezy Minimal Install <http://www.circuidipity.com/install-debian-wheezy-screenshot-tour.html>`_ and `Install Debian using grml-debootstrap <http://www.circuidipity.com/grml-debootstrap.html>`_

`c720-sidbook-post-install-main.sh <https://github.com/vonbrownie/linux-post-install/blob/master/c720-sidbook-post-install-main.sh>`_
=====================================================================================================================================

Configures the **Acer C720 Chromebook** to track Debian's *sid* branch and installs Openbox.

See: `From Chromebook to Sidbook <http://www.circuidipity.com/c720-sidbook.html>`_

Usage
=====

Download the contents of `linux-post-install <https://github.com/vonbrownie/linux-post-install>`_ (github.com/vonbrownie), navigate to the folder, and run:

.. code-block:: console

    $ cd SCRIPTS_LOCATION
    $ sudo ./SCRIPT-post-install-main.sh

Happy hacking!
