#!/usr/bin/env python

import os
import sys
import time
import datetime
import re

"""MashedPotato: An automatic JavaScript and CSS minifier

A monitor tool which checks JS and CSS files every second and
reminifies them if they've changed. Just leave it running, monitoring
your directories.

Specify a .mash file in your root directory to tell MashedPotato which
directories to monitor. See .mash_example for an example.

Usage example:

$ ./mashed_potato.py /home/wilfred/work/gxbo

To run the tests:

$ ./tests

"""

def get_paths_from_configuration(configuration_file):
    path_regexps = []
    
    for (line_number, line) in enumerate(configuration_file.split('\n')):
        line = line.strip()

        if not line.startswith('#'):
            if line:
                raw_regexp = "^" + line + "$"
                path_regexps.append(raw_regexp)

            if line.endswith('/'):
                print("Warning: directory regexps must not end with '/'. "
                      "Line %d will not do anything." % (line_number + 1)) # lines are zero-indexed

    return path_regexps

def is_being_monitored(path_regexps, directory_path):
    """Test whether this file matches any of the path regular
    expressions in the .mash configuration.
    
    """
    for regexp in path_regexps:
        if re.match(regexp, directory_path):
            return True

    return False

def is_minifiable(file_name):
    """JS or CSS files that aren't minified or hidden.

    """
    if file_name.startswith('.'):
        return False

    if not (file_name.endswith('.js') or file_name.endswith('.css')):
        return False

    if file_name.endswith('.min.js') or file_name.endswith('.min.css'):
        return False

    return True

def get_minified_name(file_path):
    """Convert a file name into its minified version. We don't do a
    simple .replace() to avoid corner cases, as shown in the example.

    >>> get_minified_name("/a/b/.js/c/foo.js)
    "/a/b/.js/c/foo.min.js"

    """
    if file_path.endswith('.js'):
        minified_path = file_path[:-3] + '.min.js'
    elif file_path.endswith('.css'):
        minified_path = file_path[:-4] + '.min.css'

    return minified_path


def needs_minifying(file_path):
    """Returns false only if a file already has a minified file, and
    the minified file is newer than the source.

    """
    source_edited_time = os.path.getmtime(file_path)

    last_minified_time = None
    minified_file_path = get_minified_name(file_path)

    if os.path.exists(minified_file_path):
        last_minified_time = os.path.getmtime(minified_file_path)

    if last_minified_time and last_minified_time > source_edited_time:
        return False

    return True


def is_ignored(file_path, ignore_strings):
    # exclude what we've been asked to ignore
    for ignore_string in ignore_strings:
        if ignore_string in file_path:
            return True
    return False


def minify(file_path):
    mashed_potato_path = os.path.dirname(__file__)

    os.system('java -jar %s/yuicompressor-2.4.5.jar %s > %s' % \
                  (mashed_potato_path, file_path,
                   get_minified_name(file_path)))


def continually_monitor_files(path_regexps, project_path):
    while True:
        time.sleep(1)

        for directory_path, subdirectories, files in os.walk(project_path):
            directory_path = directory_path[2:] # remove leading ./
            if is_being_monitored(path_regexps, directory_path):
            
                for file_name in files:
                    file_path = os.path.join(directory_path, file_name)

                    if is_minifiable(file_name) and needs_minifying(file_path):

                        minify(file_path)

                        # inform the user:
                        now_time = datetime.datetime.now().time()
                        pretty_now_time = str(now_time).split('.')[0]
                        print "[%s] Minified %s" % (pretty_now_time, file_path)


if __name__ == '__main__':
    try:
        project_path = os.path.abspath(sys.argv[1])
        configuration_path = os.path.join(project_path, ".mash")
    except IndexError:
        print "Usage: ./mashed_potato <directory containing .mash file>"
        sys.exit()

    if os.path.exists(configuration_path):
        configuration_file = open(configuration_path, 'r').read()
        path_regexps = get_paths_from_configuration(configuration_file)
    else:
        print "There isn't a .mash file at \"%s\"." % os.path.abspath(project_path)
        print "Look at .mash_example in %s for an example." % os.path.abspath(os.path.dirname(__file__))
        sys.exit()

    print "Monitoring JavaScript and CSS files for changes."
    print "Press Ctrl-C to quit or Ctrl-Z to stop."
    print ""

    try:
        continually_monitor_files(path_regexps, project_path)
    except KeyboardInterrupt:
        print "" # for tidyness' sake

