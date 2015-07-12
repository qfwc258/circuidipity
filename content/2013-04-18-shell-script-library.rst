===========================
A library for shell scripts
===========================

:date: 2013-04-18 00:11:00
:tags: shell, programming, linux
:slug: shell-script-library
:modified: 2015-07-12 13:50:00

Programming languages like Python can make use of *libraries* of code to add ready-to-go capabilities to programs. Shell scripts don't use libraries but I learned this week it is possible to *source* a file in a shell script and add functions to the script as if they were entered directly (vs spawning a subshell). Very useful in creating your own library equivalent for the shell!

There are several functions I have created in previous scripts that are self-contained in their logic and can be re-used over and over again. This function - for example - adds a test whether or not the user executing a script has root privileges:

.. code-block:: bash

    testRoot() {
    local message="$scriptName requires ROOT privileges to do its job."
    if [[ $UID -ne 0 ]]
    then
        echo -e "\n$message"
        exit 1
    fi
    }

I gathered up several other functions like this and created a **Library.sh** script that I place in my PATH. When I create a new shell script and want to access this library of functions I source it by adding:

.. code-block:: bash

    . Library.sh

... and its contents are now available for inclusion in every script that needs it. Write once and use everywhere.

Sourcing a library file for the shell reminds me of HTML templates and CSS stylesheets for websites. Adding new functions or making improvements to existing ones in a single location means the changes ripple across every script that calls upon that location.

Source: `Library.sh <https://github.com/vonbrownie/homebin/blob/master/Library.sh>`_
