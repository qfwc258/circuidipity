==========
Dot bashrc
==========

:date: 2017-06-21 09:50:00
:slug: dot-bashrc
:tags: dotfiles, shell, linux

I go ahead and customize my experience with the Bash shell by modifying the default ``~/.bashrc`` placed in $HOME by Debian!

History
-------

Disable truncating Bash history and **save it all** ...

.. code-block:: bash

    # Unlimited history.
    HISTSIZE=
    HISTFILESIZE=

Change the history file location because certain bash sessions will still try and truncate ``~/.bash_history`` upon close ...

.. code-block:: bash

    HISTFILE=~/.bash_unlimited_history

Default is to write history at the end of each session, overwriting the existing file with an updated version. If logged in with multiple sessions, only the last session to exit will have its history saved.

Configure the prompt to write to history after every command and append to the history file, don't overwrite it ...

.. code-block:: bash

    shopt -s histappend
    PROMPT_COMMAND="history -a; $PROMPT_COMMAND"

Add a timestamp per entry. Useful for context when viewing logfiles ...

.. code-block:: bash

    HISTTIMEFORMAT="%FT%T  "

Save all lines of a multiple-line command in the same history entry ...

.. code-block:: bash

    shopt -s cmdhist

Reedit a history substitution line if it failed, and edit a recalled history line before executing ...

.. code-block:: bash

    shopt -s histreedit
    shopt -s histverify

Don't put lines starting with space in the history ...

.. code-block:: bash

    HISTCONTROL=ignorespace

Toggle recording history off/on for a current shell ...

.. code-block:: bash

    alias stophistory="set +o history"
    alias starthistory="set -o history"

Helpful links! `Unlimited bash history <https://stackoverflow.com/questions/9457233/unlimited-bash-history>`_; `History truncated on each login <http://superuser.com/questions/575479/bash-history-truncated-to-500-lines-on-each-login>`_; `Preserve history in multiple terminal windows <https://unix.stackexchange.com/questions/1288/preserve-bash-history-in-multiple-terminal-windows>`_

Prompt
------

I set a two-line prompt (handy when displaying long pathnames), adjust the colour based on HOSTNAME, and if logged in remotely include an 'ssh-session' message ...

.. code-block:: bash

    if [[ -n "$SSH_CLIENT" ]]; then
        ssh_message=": ssh-session"
    fi
    if [[ $HOSTNAME = "deb"* ]] || [[ $HOSTNAME = "ull"* ]]; then
        PS1="\[\e[32;1m\]:(\[\e[37;1m\]\u@\h\[\e[33;1m\]${ssh_message}\[\e[32;1m\])-(\[\e[34;1m\]\w\e[32;1m\])\n:.(\[\e[37;1m\]\!\[\e[32;1m\])-\[\e[37;1m\]\$\[\e[0m\] "
    else
        PS1="\[\e[32;1m\]:(\[\e[31;1m\]\u@\h\[\e[33;1m\]${ssh_message}\[\e[32;1m\])-(\[\e[34;1m\]\w\e[32;1m\])\n:.(\[\e[31;1m\]\!\[\e[32;1m\])-\[\e[37;1m\]\$\[\e[0m\] "
    fi

Which generates ...

.. code-block:: bash

    :(daniel@debian)-(~)
    :.(1054)-$ ssh foobian
    :(daniel@foobian: ssh-session)-(~)
    :.(192)-$

Aliases and functions
---------------------

Enable color support of ``ls`` and a few handy aliases ...

.. code-block:: bash

    if [ -x /usr/bin/dircolors ]; then
        test -r ~/.dircolors && eval "$(dircolors -b ~/.dircolors)" || eval "$(dircolors -b)"
        alias ls="ls -aFlhv --color=auto"
        alias diff="colordiff"
        alias dir="dir --color=auto"
        alias vdir="vdir --color=auto"
        alias grep="grep --color=auto"
        alias fgrep="fgrep --color=auto"
        alias egrep="egrep --color=auto"
    fi

    # More aliases and functions.
    alias ..="cd .."
    alias aaa="sudo apt update && apt list --upgradable && sudo apt full-upgrade"
    alias arst="setxkbmap us && xmodmap ~/.xmodmap"
    alias asdf="setxkbmap us -variant colemak && xmodmap ~/.xmodmap"
    bak() { for f in "$@"; do cp "$f" "$f.$(date +%FT%H%M%S).bak"; done; }
    alias df="df -hT --total"
    alias dpkgg="dpkg -l | grep -i"
    dsrt() { du -ach $1 | sort -h; }
    alias free="free -h"
    alias gpush="git push -u origin master"
    alias gsave="git commit -m 'save'"
    alias gs="git status"
    alias histg="history | grep"
    alias lsl="ls | less"
    alias mkdir="mkdir -pv"
    mcd() { mkdir -p $1; cd $1; } 
    mtg() { for f in "$@"; do mv "$f" "${f//[^a-zA-Z0-9\.\-]/_}"; done; }
    alias pgrep="pgrep -a"
    alias psg="ps aux | grep -v grep | grep -i -e VSZ -e"
    alias tmuxa="tmux -f $HOME/.tmux.default.conf attach"
    alias wget="wget -c"
    alias zzz="sync && systemctl suspend"

Extras
------

Automatically prepend ``cd`` when entering just a path in the shell ...

.. code-block:: bash

    shopt -s autocd

`Setup keychain <http://www.circuidipity.com/secure-remote-access-using-ssh-keys.html#key-management>`_ for ssh-agent management ...

.. code-block:: bash

    if [ -x /usr/bin/keychain ]; then
        keychain ~/.ssh/id_rsa
        . ~/.keychain/$HOSTNAME-sh
    fi

Add directories to my ``$PATH`` ...

.. code-block:: bash

    export PATH=$PATH:/sbin

Disable XON/XOFF flow control ...

.. code-block:: bash

    stty -ixon

... which enables the use of ``CNTRL-S`` in other commands. **Example:** forward search in history, and disabling screen freeze in vim.

When happy with the changes, save file and reload the config ...

.. code-block:: bash

    $ source ~/.bashrc

Link: `dotfiles/.bashrc <https://github.com/vonbrownie/dotfiles/blob/master/.bashrc>`_

Happy hacking!
