# Mashed Potato

A script that monitors your directories and minifies any JS or CSS it finds.

GPL v2 license.

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

