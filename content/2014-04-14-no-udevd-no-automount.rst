======================
No udevd no auto-mount
======================

:date: 2014-04-14 01:23:00
:slug: no-udevd-no-automount
:tags: debian, linux

Problem: Auto-mounting USB storage devices fails in ``thunar`` file manager.

I ran into a situation today where changing from ``init 2`` -> ``init 1`` -> ``init 2`` failed to restart the udev daemon and rendered USB mounting non-functional.

**FIX:** Confirm ``udevd`` is running and - if not - start the daemon:

.. code-block:: bash

    $ ps ax | grep udevd
    $ sudo service udev start

... and after plugging in a USB stick additional udisk activity is generated:

.. code-block:: bash

    $ ps ax | grep udisk | awk '{print $5}'
    /usr/lib/gvfs/gvfs-udisks2-volume-monitor
    /usr/lib/udisks2/udisksd

Hope it helps!
