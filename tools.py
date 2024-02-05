import itertools
import datetime


def grouper(iterable, n, fillvalue=0):
    """ iterates and gives results with n times"""
    it = [iter(iterable)] * n
    return itertools.zip_longest(*it, fillvalue=fillvalue)


def new_file_path(file_extension, filename=''):
    now = datetime.datetime.now().strftime("%d-%m-%Y")
    if filename:
        return filename + now + file_extension
    return now + file_extension
