'''
creates the pyflakes-vim.zip bundle
'''

import os.path
import posixpath
from posixpath import curdir, sep, pardir, join

import zipfile

BUNDLE_FILENAME = 'pyflakes-vim.zip'

def get_directory():
    return os.path.abspath(os.path.dirname(__file__))

def include_dir(d):
    return not d.startswith('.git')

def include_file(f):
    return not any((f.endswith('.pyc'),
                    f.endswith('.zip'),
                    f.startswith('.git'),
                    f == __file__))

def make_dist():
    z = zipfile.ZipFile(BUNDLE_FILENAME, 'w', zipfile.ZIP_DEFLATED)
    base = get_directory()
    count = 0
    for root, dirs, files in os.walk(base):
        dirs[:] = filter(include_dir, dirs)
                
        for f in files:
            name = os.path.join(root, f)
            if include_file(f):
                zipname = relpath(name, base)
                print zipname
                count += 1
                z.writestr(zipname, open(name, 'rb').read())
    z.close()

    print
    print '%s is %d files, %d bytes' % (BUNDLE_FILENAME, count, os.path.getsize(BUNDLE_FILENAME))

def relpath(path, start=curdir):
    """Return a relative version of a path"""
    if not path:
        raise ValueError("no path specified")
    start_list = posixpath.abspath(start).split(sep)
    path_list = posixpath.abspath(path).split(sep)
    # Work out how much of the filepath is shared by start and path.
    i = len(posixpath.commonprefix([start_list, path_list]))
    rel_list = [pardir] * (len(start_list)-i) + path_list[i:]
    if not rel_list:
        return curdir
    return join(*rel_list)

if __name__ == '__main__':
    make_dist()
