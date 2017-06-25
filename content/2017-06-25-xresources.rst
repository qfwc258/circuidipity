==============
Dot Xresources
==============

:date: 2017-06-25 09:30:00
:slug: xresources
:tags: dotfiles, shell, linux

I create ``~/.Xresources`` to set my custom configuration parameters for X client applications.

Let's go!
=========

Whenever making any changes to the file, refresh the configuration by running ...

.. code-block:: bash

    $ xrdb -merge ~/.Xresources

Fonts
-----

.. code-block:: bash

    Xft.antialias:  true
    Xft.rgba:       rgb
    Xft.hinting:    true
    Xft.hintstyle:  hintslight
    
Terminal colours
----------------

I use the **Urxvt** terminal. Install (on Debian) ...

.. code-block:: bash

    $ sudo apt install rxvt-unicode-256color

Setup a colour scheme ...

.. code-block:: bash

    *foreground:       #6fc3df
    *background:       #000000
    *cursorColor:      #ef2929
    ! black
    *color0:           #000000
    *color8:           #555753
    ! red
    *color1:           #cc0000
    *color9:           #ef2929
    ! green
    *color2:           #4e9a06
    *color10:          #8ae234
    ! yellow
    *color3:           #c4a000
    *color11:          #fce94f
    ! blue
    *color4:           #3465a4
    *color12:          #025cac
    ! magenta
    *color5:           #75507b
    *color13:          #ad7fa8
    ! cyan
    *color6:           #06989a
    *color14:          #96cdfe
    ! white
    *color7:           #d3d7cf
    *color15:          #eeeeec

Terminal settings
-----------------

.. code-block:: bash

    URxvt.scrollBar: false
    URxvt.saveLines: 8888
    URxvt.font: xft:terminus:pixelsize=18
    URxvt.boldFont: xft:terminus:bold:pixelsize=18
    URxvt.perl-ext-common: default,matcher,tabbed
    URxvt.tabbed.tabbar-fg: 15
    URxvt.tabbed.tabbar-bg: 0
    URxvt.tabbed.tab-fg: 15
    URxvt.tabbed.tab-bg: 4
    URxvt.url-launcher: /usr/bin/firefox
    URxvt.matcher.button: 1
    ! add a spot of colour to man pages
    URxvt.colorIT:      #87af5f
    URxvt.colorBD:      #d7d7d7
    URxvt.colorUL:      #87afd7

Rofi
----

A `window switcher + run dialog <https://davedavenport.github.io/rofi/>`_ utility. Good stuff! Add colour ...

.. code-block:: bash

    rofi.hlfg:          #FFFFFF
    rofi.hlbg:          #FF0000

Startx
------

Add the file to ``~/.xinitrc`` for loading when executing ``startx`` ...

.. code-block:: bash

    if [ -f ~/.Xresources ]; then
        xrdb -merge ~/.Xresources
    fi

Sources: `dotfiles/.Xresources <https://github.com/vonbrownie/dotfiles/blob/master/.Xresources>`_ and `dotfiles/.xinitrc <https://github.com/vonbrownie/dotfiles/blob/master/.xinitrc>`_

Happy hacking!
