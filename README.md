# Mashed Potato

A script that monitors your directories and minifies any JS or CSS it finds. Requires Python 2.7+, no Python 3 support yet.

GPL v2 license.

## Requirements

If you're on a Mac, you'll want to have https://github.com/malthe/macfsevents installed. 
This allows MashedPotato to get notified of changed files, without having to manually poll.

##  Usage

Create a .mash file in the root of your project:

    # lines starting # are ignored
    static/js
    static/css

    # You can also use regular expression to mark your directories
    static/dev/(js|css)

    # Note you have to explicitly specify subdirectories
    static/js/[^/]*/libs
    static/js/[^/]*/libs/morelibs

Then just fire up MashedPotato, and ... that's it! MashedPotato will
monitor those directories, and automatically reminify any modified
files.

Start MashedPotato with --update-all to recompress all files that have changed since the last compression or haven't been compressed yet.
