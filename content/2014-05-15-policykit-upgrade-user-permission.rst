====================================================
Policykit upgrade generates user permission problems
====================================================

:date: 2014-05-15 01:23:00
:slug: policykit-upgrade-user-permission
:tags: debian, linux

After a recent upgrade on my 64-bit systems running Debian Sid/Unstable and Openbox I discovered user permission problems with:

* **nm-applet** - "(32) Not authorized to control networking" - refusing to make new wireless connections
* **xfce4-power-manager --dump** shows suspend/reboot/shutdown as disabled

Openbox launches with ``startx`` using ``exec ck-launch-session dbus-launch openbox-session`` in ``$HOME/.xinitrc``. Online searching for fixes generates a lot of information about policykit, consolekit, and systemd but the current problems narrowed down to the most recent upgrade of polkit-related packages in Debian.

**(Temporary) Fix:** Downgrade the problematic packages from versions ``0.105-5`` to ``0.105-4``.

**Step 0:** Removing the current polkit packages will also remove a number of related packages including network-manager and break the net connection. Previous good ``0.105-4`` versions of the affected packages were still available in ``/var/cache/apt/archives``... otherwise download packages from `snapshot.debian.org <http://snapshot.debian.org/>`_. For 64-bit amd64:

* `libpolkit-gobject-1-0:amd64 <http://snapshot.debian.org/archive/debian/20131015T214817Z/pool/main/p/policykit-1/libpolkit-gobject-1-0_0.105-4_amd64.deb>`_
* `libpolkit-agent-1-0:amd64 <http://snapshot.debian.org/archive/debian/20131015T214817Z/pool/main/p/policykit-1/libpolkit-agent-1-0_0.105-4_amd64.deb>`_
* `libpolkit-backend-1-0:amd64 <http://snapshot.debian.org/archive/debian/20131015T214817Z/pool/main/p/policykit-1/libpolkit-backend-1-0_0.105-4_amd64.deb>`_
* `policykit-1 <http://snapshot.debian.org/archive/debian/20131015T214817Z/pool/main/p/policykit-1/policykit-1_0.105-4_amd64.deb>`_

**Step 1:** Remove the troublesome packages. Take note of the dependencies also removed for later restoration:

.. code-block:: bash

    $ sudo apt-get remove libpolkit-gobject-1-0:amd64 libpolkit-agent-1-0:amd64 libpolkit-backend-1-0:amd64 policykit-1

**Step 2:** Install the downgrade packages and place them "on hold" to block ``apt-get`` from trying to upgrade again to newer (broken) versions:

.. code-block:: bash

    $ sudo dpkg -i libpolkit-gobject-1-0_0.105-4_amd64.deb
    $ sudo dpkg -i libpolkit-agent-1-0_0.105-4_amd64.deb
    $ sudo dpkg -i libpolkit-backend-1-0_0.105-4_amd64.deb
    $ sudo dpkg -i policykit-1_0.105-4_amd64.deb
    $ echo "libpolkit-gobject-1-0:amd64 hold" | sudo dpkg --set-selections
    $ echo "libpolkit-agent-1-0:amd64 hold" | sudo dpkg --set-selections
    $ echo "libpolkit-backend-1-0:amd64 hold" | sudo dpkg --set-selections
    $ echo "policykit-1 hold" | sudo dpkg --set-selections
    $ dpkg get-selections | grep "pol"  # confirm pkgs are now on hold

**Step 3:** Restore dependencies... my own system as an example:

.. code-block:: bash

    $ sudo apt-get install accountsservice colord consolekit cups-pk-helper gnome-control-center network-manager-gnome \
    packagekit packagekit-tools policykit-1-gnome upower xfce4-power-manager

Source: `UPower Suspend/Hibernate: not authorized <http://forums.debian.net/viewtopic.php?f=5&t=114412>`_
