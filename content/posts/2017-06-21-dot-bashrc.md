---
title: "Dot bashrc"
date: "2017-06-21"
publishDate: "2017-06-21"
tags:
  - dotfiles
  - shell
  - linux
slug: "bashrc"
---

I go ahead and customize my experience with the Bash shell by modifying the default `~/.bashrc` placed in $HOME.

## History

Disable truncating Bash history and **save it all** ...

```bash
# Unlimited history.
HISTSIZE=
HISTFILESIZE=
```

Change the history file location because certain bash sessions will still try and truncate `~/.bash_history` upon close ...

```bash
HISTFILE=~/.bash_unlimited_history
```

Default is to write history at the end of each session, overwriting the existing file with an updated version. If logged in with multiple sessions, only the last session to exit will have its history saved.

Configure the prompt to write to history after every command and append to the history file, don't overwrite it ...

```bash
shopt -s histappend
PROMPT_COMMAND="history -a; $PROMPT_COMMAND"
```

Add a timestamp per entry. Useful for context when viewing logfiles ...

```bash
HISTTIMEFORMAT="%FT%T  "
```

Save all lines of a multiple-line command in the same history entry ...

```bash
shopt -s cmdhist
```

Reedit a history substitution line if it failed, and edit a recalled history line before executing ...

```bash
shopt -s histreedit
shopt -s histverify
```

Don't put lines starting with space in the history ...

```bash
HISTCONTROL=ignorespace
```

Toggle recording history off/on for a current shell ...

```bash
alias stophistory="set +o history"
alias starthistory="set -o history"
```

Links: [Unlimited bash history](https://stackoverflow.com/questions/9457233/unlimited-bash-history), [History truncated on each login](http://superuser.com/questions/575479/bash-history-truncated-to-500-lines-on-each-login), and [Preserve history in multiple terminal windows](https://unix.stackexchange.com/questions/1288/preserve-bash-history-in-multiple-terminal-windows)

## Prompt

I set a two-line prompt (handy when displaying long pathnames), adjust the colour based on HOSTNAME, and if logged in remotely include an 'ssh-session' message ...

```bash
if [[ -n "$SSH_CLIENT" ]]; then
    ssh_message=": ssh-session"
fi
if [ "$color_prompt" = yes ]; then
    #PS1='${debian_chroot:+($debian_chroot)}\[\033[01;32m\]\u@\h\[\033[00m\]:\[\033[01;34m\]\w\[\033[00m\]\$ '
    PS1="${debian_chroot:+($debian_chroot)}\[\e[35;1m\]\u \[\e[37;1m\]at \[\e[32;1m\]\h\[\e[33;1m\]${ssh_message} \[\e[37;1m\]in \[\e[34;1m\]\w \n\[\e[37;1m\]\$\[\e[0m\] "
else
    PS1='${debian_chroot:+($debian_chroot)}\u@\h:\w\$ '
fi
```

## Aliases and functions

Enable color support of `ls` and a few handy aliases ...

```bash
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
alias aaa="generatePkgList -d ~/code/debian && sudo apt update && apt list --upgradable && sudo apt full-upgrade && sudo apt autoremove"
alias arst="setxkbmap us && ~/bin/keyboardconf"
alias asdf="setxkbmap us -variant colemak && ~/bin/keyboardconf"
bak() { for f in "$@"; do cp "$f" "$f.$(date +%FT%H%M%S).bak"; done; }
alias df="df -hT --total"
alias dmesg="sudo dmesg"
alias dpkgg="dpkg -l | grep -i"
alias earthview="streamlink http://www.ustream.tv/channel/iss-hdev-payload best &"
alias free="free -h"
alias gpush="git push -u origin master"
alias gsave="git commit -m 'save'"
alias gs="git status"
alias histg="history | grep"
alias mkdir="mkdir -pv"
mtg() { for f in "$@"; do mv "$f" "${f//[^a-zA-Z0-9\.\-]/_}"; done; }
alias pgrep="pgrep -a"
alias poweroff="systemctl poweroff"
alias psg="ps aux | grep -v grep | grep -i -e VSZ -e"
alias reboot="systemctl reboot"
alias shutdown="sudo /sbin/shutdown"
alias tmuxd="tmux -f ~/.tmux.default attach"
alias zzz="sync && systemctl suspend"
```

## Extras

Automatically prepend `cd` when entering just a path in the shell ...

```bash
shopt -s autocd
```

[Setup keychain](http://www.circuidipity.com/secure-remote-access-using-ssh-keys.html#key-management) for ssh-agent management ...

```bash
if [ -x /usr/bin/keychain ]; then
    keychain ~/.ssh/id_rsa
    . ~/.keychain/$HOSTNAME-sh
fi
```

Disable XON/XOFF flow control ...

```bash
stty -ixon
```

... which enables the use of `CNTRL-S` in other commands. **Example:** forward search in history, and disabling screen freeze in vim.

Set cursor colour ...

```bash
if [ -t 1 ]; then
    echo -e "\e]12;red\a"
fi
```

When happy with the changes, save file and reload the config ...

```bash
source ~/.bashrc
```

Source: [dot bashrc](https://github.com/vonbrownie/dotfiles/blob/master/.bashrc)

Happy hacking!
