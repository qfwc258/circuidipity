=====================================
Enable forward search in Bash history
=====================================

:slug: forward-search-bash
:tags: shell, linux

``CTRL-R`` enables reverse incremental searches through the Bash shell history and ``CTRL-S`` runs forward searches. However ``CTRL-S`` collides with XON/XOFF flow control in my terminal and disables that feature in history.

**Fix:** Disable XON/XOFF in ``$HOME/.bashrc``...

.. code-block:: bash

    stty -ixon

Bonus: Hitting ``CTRL-S`` by mistake in vim no longer disables output to the terminal.

Source: `Unable to forward search Bash history similarly as with CTRL-r <https://stackoverflow.com/questions/791765/unable-to-forward-search-bash-history-similarly-as-with-ctrl-r>`_
