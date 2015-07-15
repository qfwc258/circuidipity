==================================================
Vimeo and FlashBlock not playing nice on Iceweasel
==================================================

:date: 2014-01-07 01:23:00
:tags: mozilla, debian, linux
:slug: flashblock

Vimeo videos actually are not playing *at all* ... neither embedded or on the site itself.

**Fix:** Add 3 entries to the FlashBlock ``Preferences->Whitelist``:

.. code-block:: bash

    vimeo.com
    vimeocdn.com
    player.vimeo.com

Works on ``Iceweasel 24.2.0`` with ``Flashblock 1.5.17`` .
