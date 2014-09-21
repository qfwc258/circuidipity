======================================================
Video2Audio - Search for video and copy/convert to MP3
======================================================

:date: 2013-03-28 01:23:00
:tags: shell, programming, linux
:slug: video2audio

I think I have discovered the secret to learning to  program. Write programs!

... *(cue applause) Thank you for coming don't forget to tip your server and good-night to all ...*

OK. Perhaps a bit more explanation. Great programming books and online resources and sample problems are *accelerants* but trying to program a solution to your *own private thing* is the *spark*. Write a bit of code every day that you need and that *pushes* the learning engine ever higher and makes it stutter stop start in the rarified air. Feel the wonderful little jolts to the brain when the code *works*. Then do it *again*. Spark. Code. Repeat.

Building on what I learned last week using the ``find`` command in `tarTime <http://www.circuidipity.com/tartime-find-time-tar.html>`_ I thought ... *How about a shell script that would allow me to find a bunch of videos accumulated over TIME and would copy/convert them to MP3 audio? Or instead of TIME as my search parameter maybe only certain TYPES of video or use both TIME and TYPE*. Example: only convert MP4 videos modified in the last 3 days?

So I wanted to code a shell script that would:

* copy/convert either a single video or a batch of videos that satisfy a SEARCH paramater
* SEARCH using *find* for videos modified since TIME and/or of a certain TYPE (MP4,FLV, etc.)
* list all the matching files or ...
* ... convert to MP3

*Update 2013-04-04:* Used ``set noglob`` to forego wildcard expansion of NAME arguments that broke find command's recursive search, added a counter function to return total number of videos returned by find, and the ``getopts`` shell built-in to process positional parameters and their arguments.

.. code-block:: bash

    #!/bin/bash
    #: VARIABLES
    Scriptname="Video2Audio"
    Description="Recursive search of PWD for video and copy/convert to MP3"
    Synopsis="$Scriptname [-v|-h|-a|-n [FILE]|-t [+-][TIME]]"
    # -------- #
    RequiredPrograms="findutils, ffmpeg, libmp3lame0"
    InvalidInput="is invalid input. Please select 'Y(es)' or 'N(o)' ..."
    Codecs="MP4:FLV:AVI:M4V:MKV:MOV:WMV"
    Converter="ffmpeg"
    Mp3Config="-acodec libmp3lame -aq 0 -ac 2 -ar 44100"
    InameList=( -iname \*.mp4 -o -iname \*.flv -o -iname \*.avi -o -iname \*.m4v -o -iname \*.mkv -o -iname \*.mov -o -iname \*.wmv )
    FindNameAll="*"
    FindName=
    FindTime=

    #: FUNCTIONS
    VersionInfo()
    {
    cat << _EOF_
    $Scriptname, Version $Version
    _EOF_
    }

    HelpInfo()
    {
    cat << _EOF_
    Usage: $Synopsis
    ${Description}. Supported Codecs: $Codecs

    Debian package requirements: $RequiredPrograms

    OPTIONS
    -v  display version
    -h  display help
    -t  match videos last modified [+-][digit][m[inutes]|d[ays] ago
    -n  match video NAME
    -a  match all videos

    EXAMPLES
    # convert a single video
    Video2Audio -n VIDEO1.mp4

    ... or batch-convert ...

    # convert videos modified less than 30 minutes ago
    Video2Audio -t -30m 
    # convert videos modified more than 5 days ago
    Video2Audio -t +5d 
    # convert all MP4-encoded videos (quotes are important)
    Video2Audio -n "*mp4"
    # convert all FLV-encoded videos modified less than 90 minutes ago
    Video2Audio -n "*flv" -t -90m 
    # convert all videos
    Video2Audio -a
    _EOF_
    }

    ModField()
    {
    if [[ -z $FindTime ]]
    then
        ModUnits=""
    else
        if [[ $FindTime =~ ^[+-]*[0-9]+[m]$ ]]
        then
                ModUnits="-mmin ${FindTime%m}"
        elif [[ $FindTime =~ ^[+-]*[0-9]+[d]$ ]]
        then
                ModUnits="-mtime ${FindTime%d}"
        else
                printf "Error: '-t' option requires argument in correct format ...\n"
                printf "\n"
                HelpInfo
                exit 1
        fi
    fi
    }

    Penguinista()
    {
    cat << _EOF_

    (O<
    (/)_
    _EOF_
    }

    FindNameCount()
    {
    set -o noglob   # no pathname expansion
    ModField
    local counter
    counter=/tmp/FindNameCount
    find -L . -iname $FindName -type f $ModUnits -print 2>/dev/null | tee -a $counter
    printf "Found $( wc -l $counter | awk {'print $1'} ) file(s).\n"
    rm $counter
    set +o noglob
    }

    FindTimeCount()
    {
    ModField
    local counter
    counter=$( find -L . \( "${InameList[@]}" \) -type f $ModUnits -print 2>/dev/null | tee /dev/tty | wc -l )
    printf "Found $counter file(s).\n"
    }

    #: LET'S ROLL ...
    if [[ $1 != "" ]]
    then
        while getopts “n:t:ahv” OPTION
        do
                case $OPTION in
                        a )     FindName=$FindNameAll
                                break
                                ;;
                        n )     FindName=$OPTARG
                                ;;
                        t )     FindTime=$OPTARG
                                ;;
                        h )     HelpInfo
                                exit
                                ;;
                        v )     VersionInfo
                                exit
                                ;;
                        ? )     HelpInfo
                                exit 1
                                ;;
                esac
        done
    else
        printf "Error: Video2Audio requires at least 1 parameter ...\n"
        printf "\n"
        HelpInfo
        exit 1
    fi

    if [[ ( -n $FindTime && -n $FindName ) || -n $FindName ]]
    then
        FindNameCount
        while true
        do
                printf "\n"
                read -n 1 -p "Copy/convert videos to MP3? [Yn] > "
                if [[ "$REPLY" == [Yy] || "$REPLY" == "" ]]
                then
                        find -L . -iname "$FindName" -type f $ModUnits \
                                -exec $Converter -i '{}' $Mp3Config '{}'.mp3 \; \
                                -exec sh -c 'mv "$0" "${0%.*.mp3}.mp3"' '{}'.mp3 \;
                                # file name {} passed to shell as its 0th argument and
                                # script uses shell variable $0 to refer to the file
                        printf "\n"
                        printf "$(Penguinista)  All done.\n"
                        exit
                elif [[ "$REPLY" == [nN] ]]
                then
                        printf "\n"
                        printf "$(Penguinista)  OK. Nothing done.\n"
                        exit
                else
                        printf "\n"
                        printf "'$REPLY' $InvalidInput\n"
                fi
        done
    fi

    if [[ -n $FindTime ]]
    then
        FindTimeCount
        while true
        do
                printf "\n"
                read -n 1 -p "Copy/convert videos to MP3? [Yn] > "
                if [[ "$REPLY" == [Yy] || "$REPLY" == "" ]]
                then
                        find -L . \( "${InameList[@]}" \) -type f $ModUnits \
                                -exec $Converter -i '{}' $Mp3Config '{}'.mp3 \; \
                                -exec sh -c 'mv "$0" "${0%.*.mp3}.mp3"' '{}'.mp3 \;
                        printf "\n"
                        printf "$(Penguinista)  All done.\n"
                        exit
                elif [[ "$REPLY" == [nN] ]]
                then
                        printf "\n"
                        printf "$(Penguinista)  OK. Nothing done.\n"
                        exit
                else
                        printf "\n"
                        printf "'$REPLY' $InvalidInput\n"
                fi
        done
    fi

Examples
========

Video2Audio can copy/convert videos to MP3 either one at a time ``Video2Audio -n VIDEO1.mp4`` or perform a batch-conversion that satisfies a SEARCH paramater ...

.. code-block:: bash

    # convert videos modified less than 30 minutes ago
    $ Video2Audio -t -30m 

    # convert videos modified more than 5 days ago
    $ Video2Audio -t +5d 

    # convert all MP4-encoded videos (quotes are important)
    $ Video2Audio -n "*mp4"

    # convert all FLV-encoded videos modified less than 90 minutes ago
    $ Video2Audio -n "*flv" -t -90m 

    # convert all videos
    $ Video2Audio -a

Running ``Video2Audio -h`` displays available options.

This week I learned about *bash arrays*. They allow you to assign multiple values to a variable. I used them twice in this shell script: 1/ to list video FILETYPES for *find*; 2/ to construct a list of NAMES of videos to be converted to audio. Also the find *exec* option is put to good use and trying to get the syntax right for file manipulation is a bit of a puzzle.

But it *works*. I use this script to generate MP3 files and `tarTime <http://www.circuidipity.com/tartime-find-time-tar.html>`_ to bundle them up into a single convenient package.
