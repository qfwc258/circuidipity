===========================
A library for shell scripts
===========================

:tags: shell, programming, linux
:slug: shell-script-library

Programming languages like Python can make use of *libraries* of code to add ready-to-go capabilities to programs. Shell scripts don't use libraries but I learned this week it is possible to <strong>source</strong> a file in a shell script and add functions to the script as if they were entered directly (vs spawning a subshell). Very useful in creating your own library equivalent for the shell!

There are several functions I have created in previous scripts that are self-contained in their logic and can be re-used over and over again. This function - for example - adds a test whether or not the user executing a script has root privileges ...

.. code-block:: bash

    ConfirmRoot()
    {
    if [[ $UID -ne 0 ]]
    then
        printf "\n$( Penguinista )\t$Scriptname requires ROOT privileges to do its job.\n"
    exit
    fi
    }

*Penguinista* is another function that draws a little ASCII penguin and *Scriptname* is a variable that holds - you guessed it - the script's name and is present in every script I write. I gathered up several other functions like this adding them to a ``Library.sh`` file and placing it in my PATH. When I create a new shell script and want to access this library of functions I source *Library.sh* by adding ...

.. code-block:: bash

    . Library.sh

``ConfirmRoot`` is now available for inclusion in every script that needs it ... write once and use everywhere. Sourcing a library file for the shell reminds me of HTML templates and CSS stylesheets for websites. Adding new functions or making improvements to existing ones in a single location means the changes ripple across every script that calls upon that location.
