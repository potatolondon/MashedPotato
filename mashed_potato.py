#!/usr/bin/env python

import os
import sys
import time

"""MashedPotato: An automatic JavaScript minifier

A monitor tool which checks JS files every second and reminifies them
if they've changed. Just leave it running, monitoring your
directories.

Usage example:

$ ./mashed_potato "../static/js" "../static/js/more"

"""

def is_minifiable(file_name):
    """JS files that aren't yet minified or hidden.

    """
    if file_name.startswith('.'):
        return False

    if not file_name.endswith('.js'):
        return False

    if file_name.endswith('.min.js'):
        return False

    return True

def minify(js_file_path):
    minified_file_path = js_file_path.replace('.js', '.min.js')
    os.system('java -jar yuicompressor-2.4.2.jar %s > %s' % \
                  (js_file_path, minified_file_path))


if __name__ == '__main__':
    javascript_directories = sys.argv[1:]

    if not javascript_directories:
        print "Usage: ./mashed_potato <JavaScript directory 1> <JavaScript directory 2> ..."
        sys.exit()
    else:
        print "Monitoring JavaScript for changes. Press Ctrl-C to quit."

    minified_times = {}

    while True:
        time.sleep(1)

        for directory in javascript_directories:
            for file_name in os.listdir(directory):
                # todo: use os.path.join
                file_path = os.path.join(directory, file_name)

                if is_minifiable(file_name):
                    modified_time = os.path.getmtime(file_path)
                    minified_time = minified_times.get(file_path, None)

                    if not minified_time or modified_time > minified_time:
                        minified_times[file_path] = modified_time
                        minify(file_path)
