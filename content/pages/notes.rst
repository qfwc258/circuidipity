=====
Notes
=====

:slug: notes

2017-06-08T0920
---------------
**[x]** Attaching to a wifi network with ``nmcli`` (network-manager cli client) ...

.. code-block:: bash

    $ nmcli radio
    $ nmcli device
    $ nmcli device wifi rescan
    $ nmcli device wifi connect SSID-Name password PASS

2017-06-07T1219
---------------
**[x]** Disable `Pelican <http://www.circuidipity.com/tag-pelican.html>`_ from auto-generating ``archives.html`` by adding to ``pelicanconf.py`` ...

.. code-block:: bash

    ARCHIVES_SAVE_AS = ''

From `URL Settings <http://docs.getpelican.com/en/latest/settings.html#url-settings>`_: "If you do not want one or more of the default pages to be created ... set the corresponding ``*_SAVE_AS`` setting to '' to prevent the relevant page from being generated."
