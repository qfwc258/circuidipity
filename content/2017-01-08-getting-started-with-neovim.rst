===========================
Getting started with Neovim
===========================

:date: 2017-01-08 19:18:00
:slug: neovim
:tags: neovim, vim

Text-wrangling is a big part of unlocking the power of Linux and programming ... and with great power comes the need for a great text editor!

I have used **Vim** in the past but barely scratched the surface of its features motherlode. A friend who is a `passionate vim user <http://gilesorr.com/blog/tag/vim.html>`_ recommended I try **Neovim**, which "*strives to be a superset of Vim except for some intentionally-removed misfeatures... [and] is built for users who want the good parts of Vim, and more*". Sounds good!

0. Install Neovim
-----------------

Neovim packages are available for **Ubuntu Linux** courtesy of a *Personal Package Archive (PPA)* ...

.. code-block:: bash

	$ sudo apt install software-properties-common
	$ sudo add-apt-repository ppa:neovim-ppa/unstable
	$ sudo apt update
	$ sudo apt install neovim
	$ sudo apt install python-dev python-pip python3-dev python3-pip

1. Launch
---------

Start the newly-installed editor ...

.. code-block:: bash

	$ nvim

Upon first launch on Ubuntu the ``~/.local/share/nvim/{shada,swap}`` directories are auto-generated. Manually create a new ``~/.config/nvim`` configuration directory and place inside an ``init.vim`` config file (or link to an existing ``~/.vimrc``) ...

.. code-block:: bash

	$ mkdir ~/.config/nvim
	$ cd ~/.config/nvim
	$ ln -s ~/.vimrc init.vim

Check out Neovim's built-in ``:help`` command and the `online documentation <https://neovim.io/doc/>`_ .

Source: https://github.com/vonbrownie/dotfiles/blob/master/.config/nvim/init.vim

2. Plugins
----------

Extend the core features of the text editor using **plugins**. With a fresh install of Neovim, now is a good time to setup a plugin manager. I install `Vundle <https://github.com/VundleVim/Vundle.vim>`_ ...

.. code-block:: bash

	$ git clone https://github.com/VundleVim/Vundle.vim.git ~/.config/nvim/bundle/Vundle.vim

Configure neovim to use vundle by modifying ``~/.config/nvim/init.vim`` ...

.. code-block:: bash

    set nocompatible
    filetype off
    " set the runtime path to include Vundle and initialize
    set rtp+=~/.config/nvim/bundle/Vundle.vim
    call vundle#begin()
    " let Vundle manage Vundle, required
    Plugin 'VundleVim/Vundle.vim'
    " All of your Plugins must be added before the following line
    call vundle#end()
    filetype plugin indent on  " allows auto-indenting depending on file type
    
Install plugins ...

.. code-block:: bash

	$ nvim +PluginInstall +qall

Happy hacking!
