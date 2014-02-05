============================================
DualDisplay - Extended desktop configuration
============================================

:tags: shell, programming, linux
:slug: dual-display-xrandr-extended-desktop-configuration

Bash shell scripting strikes me as a good place for a Linux user to start to learn programming. Diving into the command line unlocks the power of Linux, makes it malleable to the user, and you pick up some history of how Unix came to be what it is today. Design ideas like *everything is a file* and *pipes* are incredibly useful for taking simple discrete components and stringing them together to build something new and awesome!

I am working my way through `The Linux Command Line <http://linuxcommand.org/tlcl.php>`_ and I love it! Starting with a gentle introduction and configuration of the Bash shell, then quickly moving on to exploring the filesystem, input and output and redirection, manipulating text with *vim* and *regular expressions* and a whole suite of simple utilities (that can be piped to direct the flow of data into executing tasks of increasing complexity), finally bringing it all together in the latter part of the book to start assembling these commands together via *shell scripting*.

When I am at home I connect an external display to my Thinkpad to create an *extended desktop* (running the *Openbox* window manager). I thought, *How cool would it be to have a shell script that auto-detected and configured the external display at startup?*

So I used some new tricks gleaned from *TLCL* to create ``dualDisplay``. I required a script that would:

* parse output of ``xrandr`` to *detect* PRIMARY (and possible SECOND) displays connected to HOST
* *if* SECOND *then create* an extended desktop using PRIMARY + SECOND
* use a *positional parameter* to provide option to *disable* extended desktop
* create a *test* to give the user feedback if an incorrect option is used

.. code-block:: bash

    #!/bin/bash
    # Enable|disable extended desktop using XRandR

    PRIMARY=$(xrandr | grep " connected" | awk 'FNR == 1 {print $1}')
    SECOND=$(xrandr | grep " connected" | awk 'FNR == 2 {print $1}')
    CONFIG="xrandr --output $PRIMARY --auto --primary --output $SECOND"

    if [[ -n $SECOND ]]; then
        if [ "$1" != "" ]; then
            case $1 in
                -q )    $CONFIG --off
                        exit
                        ;;
                * )     printf "ERROR: '$1' is an invalid option\n"
                        printf "Option: '-q' disables an extended desktop\n"
                        exit 1
                        ;;
            esac
        else
            $CONFIG --auto --right-of $PRIMARY
        fi
    fi

Make the script executable and drop it in ``$HOME/bin``.

Run ``dualDisplay`` or ``dualDisplay -q`` at the command line to enable|disable PRIMARY + SECOND. For Openbox I add the command to ``~/.config/openbox/autostart`` and now it launches and stitches together the Thinkpad's LCD and external display into a extended desktop whenever I enter the X environment.
