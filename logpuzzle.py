#!/usr/bin/env python
"""
Logpuzzle exercise

Copyright 2010 Google Inc.
Licensed under the Apache License, Version 2.0
http://www.apache.org/licenses/LICENSE-2.0

Google's Python Class
http://code.google.com/edu/languages/google-python-class/

Given an apache logfile, find the puzzle urls and download the images.

Here's what a puzzle url looks like:
10.254.254.28 - - [06/Aug/2007:00:13:48 -0700] "GET /~foo/puzzle-bar-aaab.jpg HTTP/1.0" 302 528 "-" "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.6) Gecko/20070725 Firefox/2.0.0.6"

"""


import os
import re
import sys
import urllib
import argparse
import timeit




def read_urls(filename):
    url_list = []
    """Returns a list of the puzzle urls from the given log file,
    extracting the hostname from the filename itself.
    Screens out duplicate urls and returns the urls sorted into
    increasing order."""
    with open(filename, "r") as f:
        read = f.readlines()
        for url_line in read:
            finder = re.search(r'GET\s(\S+)\sHTTP', url_line)
            url_list.append('http://code.google.com' + finder.group(1))
        # for i in url_list:
        #     print(i)
        url_list = sorted(list(set(url_list)))
        return url_list


def download_images(img_urls, dest_dir):
    """Given the urls already in the correct order, downloads
    each image into the given directory.
    Gives the images local filenames img0, img1, and so on.
    Creates an index.html in the directory
    with an img tag to show each local image file.
    Creates the directory if necessary.
    """
    if not os.path.isdir(dest_dir):
        os.mkdir(dest_dir)
    if not os.path.exists(dest_dir + 'index.html'):
        with open(dest_dir + '/index.html', "w") as f:
            pass

    for index, url in enumerate(img_urls):
        filename = dest_dir + '/img' + str(index)
        urllib.urlretrieve(url, filename)
        with open(dest_dir + '/index.html', "a") as f:
            f.write('<img src="../animaldir/img' + str(index) + '"' + '/>' + '\n')



# def timeit_helper():
#     """Part A:  Obtain some profiling measurements using timeit"""
#     t = timeit.Timer('read_urls("animal_code.google.com")')
#     result = t.repeat(repeat=5, number=3)
#     avg_list = []
#     for clock in result:
#         avg_list.append(clock/3)
#     average = min(avg_list)
#     print('Best time across 5 repeats of 3 runs per repeat:{} sec'.format(average))


def create_parser():
    """Create an argument parser object"""
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--todir',  help='destination directory for downloaded images')
    parser.add_argument('logfile', help='apache logfile to extract urls from')

    return parser



def main(args):
    """Parse args, scan for urls, get images from urls"""
    parser = create_parser()

    if not args:
        parser.print_usage()
        sys.exit(1)

    parsed_args = parser.parse_args(args)

    img_urls = read_urls(parsed_args.logfile)

    if parsed_args.todir:
        download_images(img_urls, parsed_args.todir)
        # timeit_helper()
    else:
        print('\n'.join(img_urls))


if __name__ == '__main__':
    main(sys.argv[1:])
