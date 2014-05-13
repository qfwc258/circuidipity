================================
Creating new commands with alias
================================

:slug: alias-commands
:tags: shell, linux

An **alias** is useful for setting desirable options for a shell command or creating new commands using the structure ``alias name='string``. Multiple commands can be placed on a single line by separating them with a semicolon ``alias name='command0; command1; command2``.

Check for aliases already set in the environment:

.. code-block:: bash

        $ alias

Remove the alias for command ``foo``:

.. code-block:: bash

        $ unalias foo

Create new aliases:

.. code-block:: bash

        $ alias ls='ls -aFlhv --color=auto'
        $ alias dpkgg='dpkg -l | grep'
        $ alias aaa='sudo apt-get update; sudo apt-get dist-upgrade; sudo apt-get autoremove'
        $ type ls   # display information about a command
        ls is aliased to `ls -aFlhv --color=auto'

Aliases created at the prompt persist only for the duration of the current session. Make them permanent by adding them to ``$HOME/.bashrc``. Examples:

.. code-block:: bash

        alias df='df -hT'
        alias diff='colordiff'
        alias dpkgg='dpkg -l | grep'
        alias grep='grep --color=auto'
        alias halt='systemctl poweroff'
        alias mkdir='mkdir -p -v'
        alias psg='ps aux | grep'
        alias pwd='pwd -P'
        alias reboot='systemctl reboot'
        alias suspend='systemctl suspend'

Happy hacking!
