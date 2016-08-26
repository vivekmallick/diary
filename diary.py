#!/usr/bin/python

import time

def extract_time_file_name():
    """
    Checks the current time and returns a string which will form the
    initial part of the file name.
    """

    timestr = time.strftime('%Y%m%d_%H%M')
    return timestr

def extract_time_header():
    """Returns a time stamp to be used as the header."""

    return time.ctime()

print extract_time_file_name()
print extract_time_header()
