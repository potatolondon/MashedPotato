#!/usr/bin/env python

import os
import sys
import time
import datetime

"""MashedPotato: An automatic JavaScript and CSS minifier

A monitor tool which checks JS and CSS files every second and
reminifies them if they've changed. Just leave it running, monitoring
your directories.

Usage example:

$ ./mashed_potato "../static/js" "../static/js/more"

"""

mashed_potato_path = os.path.dirname(__file__)

def is_minifiable(file_name):
    """JS or CSS files that aren't yet minified or hidden.

    """
    if file_name.startswith('.'):
        return False

    if not (file_name.endswith('.js') or file_name.endswith('.css')):
        return False

    if file_name.endswith('.min.js') or file_name.endswith('.min.css'):
        return False

    return True

def is_ignored(file_path, ignore_strings):
    # exclude what we've been asked to ignore
    for ignore_string in ignore_strings:
        if ignore_string in file_path:
            return True
    return False


def minify(file_path):
    if file_path.endswith('.js'):
        minified_file_path = file_path.replace('.js', '.min.js')
    else:
        minified_file_path = file_path.replace('.css', '.min.css')

    os.system('java -jar %s/yuicompressor-2.4.5.jar %s > %s' % \
                  (mashed_potato_path, file_path, minified_file_path))


if __name__ == '__main__':
    arguments = sys.argv[1:]

    if '--ignore' in arguments:
        flag_position = arguments.index('--ignore')
        javascript_directories = arguments[:flag_position]
        ignore_strings = arguments[flag_position+1:]
    else:
        javascript_directories = arguments
        ignore_strings = []

    if not javascript_directories:
        print "Usage: ./mashed_potato <directory 1> <directory 2> ... [--ignore <script or folder names>]"
        sys.exit()
    else:
        print "Monitoring JavaScript and CSS files for changes.\nPress Ctrl-C to quit or Ctrl-Z to stop.\n"

    minified_times = {}

    while True:
        time.sleep(1)

        for directory in javascript_directories:
            for path, subdirs, files in os.walk(directory):
                for file_name in files:
                    file_path = os.path.join(path, file_name)

                    if is_minifiable(file_name) and not is_ignored(file_path, ignore_strings):
                        modified_time = os.path.getmtime(file_path)
                        minified_time = minified_times.get(file_path, None)

                        if not minified_time or modified_time > minified_time:
                            minified_times[file_path] = modified_time
                            minify(file_path)

                            # inform the user:
                            now_time = datetime.datetime.now().time()
                            pretty_now_time = str(now_time).split('.')[0]
                            print "[%s] Minified %s" % (pretty_now_time, file_path)
