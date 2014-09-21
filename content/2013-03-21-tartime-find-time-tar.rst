================================================
TarTime - Match files and generate a tar archive
================================================

:date: 2013-03-21 01:23:00
:tags: shell, programming, linux
:slug: tartime-find-time-tar

If you are going to perform some multi-step action on the Linux command line more than once or twice ... why not create a *shell script*?

Scripting poses the question *What am I trying to accomplish?* then provides a framework for sketching a logical flow of operations to make it so. I am discovering it is a fun puzzle trying to get the friendly but simple computer and I to agree on what is logical. End result is a well-tested scripted solution that can be automated out of sight, saves time (or do we just tell ourselves that because its fun?) and reduces error vs manual entry of commands.

Often I want to share files accumulated over a specific period of time. I thought ... *How about a shell script that would allow me to input a TIME and it would find all files last modified since TIME then copy and bundle them up into a tar archive?* Example: I might want to share with a friend all the photos I have accumulated on my hard drive since we last met 2 weeks ago. All the photos are in my *images* folder but underneath that are scattered among various sub-folders.

Building on what I learned last week creating `dualDisplay <http://www.circuidipity.com/dual-display-xrandr-extended-desktop-configuration.html>`_ I required a script that would:

* allow me to define a period of TIME in *minutes* or *days*
* use ``find`` to *recursively* match all files last modified since TIME
* list all the matching files or ...
* ... copy and create the tar archive (with an option to *compress* the contents)

One element I found a bit tricky was sorting out the use of *regular expressions* and *globbing* in creating positional parameters for matching relevant files ... ``man 7 glob``, this `tutorial <http://www.linuxjournal.com/content/bash-extended-globbing>`_, and my local `LUG <http://gtalug.org/wiki/Main_Page>`_ were a big help.

So this is **tarTime** ... a Bash shell script that matches files recursively from the current directory that were last modified [+-TIME] ago and generates a tar archive ...

.. code-block:: bash

    #!/bin/bash

    #: VARIABLES
    filename=$(basename $(pwd).$(date +%F.%H%M%S).tar)

    #: FUNCTIONS
    helpInfo () {
    		cat << _EOF_
    Usage: tarTime [OPTION] [+-TIME]
    Match files recursively from current directory that were last modified [+-TIME] ago and generate a tar archive.

    OPTIONS
    -[digit][m[inutes]|d[ays], +[digit][m[inutes]|d[ays]]
    	match files whose contents were last modified [TIME] ago
    -a, --all
	match all files
    -z, --compress
	compress tar archive using gzip
    -l, --list
	only list files that match find search parameters

    Examples:
	TarTime -7d   		# match files < 7 days old and generate tar archive
	TarTime +7d  		# match files > 7 days old and generate tar archive
	TarTime -88m		# match files < 88 minutes old and generate tar archive
	TarTime -l -7d		# only list files < 7 days old
	TarTime --all		# match all files and generate tar archive
    _EOF_
    }

    searchMethod () {
    	    if [[ $searchLimit =~ [m]$ ]]; then
	        findTime="find . -type f -mmin ${searchLimit%m}"
	    elif [[ $searchLimit =~ [d]$ ]]; then
		findTime="find . -type f -mtime ${searchLimit%d}"
	    else
		findTime="find . -type f"
	    fi
    }

    penguinista () {
	    cat << _EOF_

    (O<
    (/)_
    _EOF_
    }

    #: LET'S ROLL ...
    # enable extended globbing for 'searchLimit=' match - see 'man 7 glob'
    shopt -s extglob

    # '$#' is a shell variable containing total number of items on command line minus the command($0) itself
    # 'shift' is a shell builtin that shifts all the positional parameters down by one
    if [[ $1 != "" ]]; then
	while [[ $# -gt 0 ]]; do
	    case $1 in
		[+-]+([0-9])[md] | -a | --all )     searchLimit=$1
						    searchMethod
						    shift
						    ;;
		-l | --list )			    listOnly=1
						    shift
						    ;;
		-z | --compress )		    compress=1
						    shift
						    ;;
		-h | --help )			    helpInfo
						    exit
						    ;;
                * )				    echo "ERROR: Invalid option(s) specified ..."
						    echo ""
						    helpInfo
						    exit 1
						    ;;
	        esac
	    done
    else
	echo "ERROR: tarTime requires at least 1 parameter ..."
	echo ""
	helpInfo
	exit 1
    fi

    if [[ $listOnly -eq 1 ]]; then
	echo "These are the files that will be copied to the tar archive ..."
	echo ""
	$findTime
    else
	if [[ $compress -eq 1 ]]; then
	    $findTime -exec tar -czf ${filename}.gz '{}' \+
	else
	    $findTime -exec tar -cf $filename '{}' \+
	fi
	echo "$(penguinista)  '$(ls -t *.tar* | head -n 1 | awk ' { print ( $(NF) ) }')' was generated."
    fi

Examples
========

If I wanted to share all photos created in the last 2 weeks I would navigate to the images directory and run ``tarTime -14d``. The script would recursively match all photos from the last 14 days and generate a tar archive labelled ``FOLDER.DATE.TIME.tar`` or ``.tar.gz`` if compressed.

Some other uses ...

.. code-block:: bash

    # tar files modified more than 7 days ago
    $ tarTime +7d

    # tar files modified less than 88 minutes ago
    $ tarTime -88m

    # list files modified less than 7 days ago
    $ tarTime -l -7ds

    # tar all files
    $ tarTime --all

Running ``tarTime --help`` displays available options.
