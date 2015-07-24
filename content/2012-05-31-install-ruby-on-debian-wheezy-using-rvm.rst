================================
Install Ruby on Debian using RVM
================================

:date: 2012-05-31 01:23:00
:tags: ruby, programming, rvm, debian, linux
:slug: install-ruby-on-debian-wheezy-using-rvm

I have a small bit of shell scripting fu and have acquired the taste for more programming. `Ruby <http://www.ruby-lang.org/en/>`_ has the reputation for being a friendly language to newbies and I have decided to give it a go.

There are a few `different methods <http://www.ruby-lang.org/en/downloads/>`_ for installing Ruby on Debian Wheezy ... I opted to use a third-party tool called the *Ruby enVironment Manager* (`RVM <https://rvm.io/>`_). Grabbing the latest version of Ruby + the ability to host multiple, self-contained Ruby installations is made easier with RVM.

Installing RVM for the use of a single user creates ``~/.rvm`` to hold all the Ruby-related files. `Get started <https://rvm.io/rvm/install/>`_ by downloading ``curl -L get.rvm.io | bash -s stable``.

Load RVM ``source ~/.rvm/scripts/rvm``.

Check for additional requirements ``rvm requirements``.

I needed to install these extras ...

.. code-block:: bash

    $ sudo apt-get install build-essential openssl libreadline6 libreadline6-dev curl git-core zlib1g zlib1g-dev libssl-dev libyaml-dev libsqlite3-dev sqlite3 libxml2-dev libxslt-dev autoconf libc6-dev ncurses-dev automake libtool bison subversion

Now I can use RVM to install the latest stable version of Ruby ``rvm install 1.9.3``.

The current system-wide install of Ruby is ``1.8.7.352-2`` ... To test my new RVM configuration and confirm that I am using my later, freshly-installed version I run:

.. code-block:: bash

    $ type rvm | head -n 1
    rvm is a function
    $ ruby -v
    ruby 1.9.3p194 (2012-04-20 revision 35410) [x86_64-linux]
    $ which ruby
    /home/dwa/.rvm/rubies/ruby-1.9.3-p194/bin/ruby

It works. Good!

But not for long. I ran into two problems: trying to load RVM as a shell function failed to work in new shells, and I discovered that login shells were no longer reading ``~/.bashrc`` settings.

RVM made two modifications that in Debian Wheezy need to be altered:

* it created ``~/.bash_login`` which blocked ``~/.profile`` from being read (and stopped ``~/.bashrc`` from being used)
* it created a new PATH in ``.bashrc``

**To Fix:**

1/ Copy the RVM function in ``~/.bash_login`` ...

.. code-block:: bash

    [[ -s "$HOME/.rvm/scripts/rvm" ]] && . "$HOME/.rvm/scripts/rvm"

... and place it at the end of ``~/.bashrc``

2/ Remove ``~/.bash_login``

3/ Edit the PATH setting to include extra directories

Now it works. Good good!

Reference:

* ``~/.rvm/bin/rvm`` Vs ``~/.rvm/scripts/rvm`` - http://stackoverflow.com/questions/10513925/rvm-bin-rvm-vs-rvm-scripts-rvm

* `The Basics of RVM <https://rvm.io/rvm/basics/>`_
