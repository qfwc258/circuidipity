==========================================
Multiple instances of nm-applet in Openbox
==========================================

:tags: openbox, linux
:slug: nm-applet-openbox

I had commented out my entry for ``nm-applet`` in ``$HOME/.config/openbox/autostart`` and system was loading ``nm-applet`` from ``/etc/xdg/autostart/nm-applet.desktop``. Problem: After updating Openbox there were *two* instances of ``nm-applet`` being loaded.

In ``/usr/lib/x86_64-linux-gnu/openbox-autostart`` ...

.. code-block:: bash

    GLOBALAUTOSTART="/etc/xdg/openbox/autostart"
    AUTOSTART="${XDG_CONFIG_HOME:-"$HOME/.config"}/openbox/autostart"

**Fix:** Edited ``/etc/xdg/autostart/nm-applet.desktop`` to read ...

.. code-block:: bash

    NotShowIn=KDE;GNOME;OPENBOX;

... and *no* ``nm-applet`` appears when Openbox is loaded. Re-enabled ``nm-applet`` in ``autostart`` ...

.. code-block:: bash

    (sleep 3 && /usr/bin/nm-applet --sm-disable) &

... re-started Openbox and now only the desired *single* instance of ``nm-applet`` is loaded.
