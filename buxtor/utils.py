import itertools
import os


def grouper(iterable, n, fillvalue=None):
    "Collect data into fixed-length chunks or blocks"
    # grouper('ABCDEFG', 3, 'x') --> ABC DEF Gxx"
    args = [iter(iterable)] * n

    return itertools.zip_longest(*args, fillvalue=fillvalue)


def walk_dir(start_path):
    """Yields paths for the contents of a directory. The paths are relative to
    the starting directory.

    All directories and hidden files are ignored.
    """
    for root, dirs, files in os.walk(start_path):
        dirs[:] = [d for d in dirs if not d.startswith('.')]
        files = [f for f in files if not f.startswith('.')]

        for f in files:
            name = os.path.join(root, f)
            yield os.path.relpath(name, start_path)


def path_components(path):
    """Returns a list of components of a path.

    >>> path_components('/foo/bar')
    ['/', 'foo', 'bar']
    """
    components = []

    while True:
        dirname, basename = os.path.split(path)

        if basename:
            components.append(basename)

        if (dirname, basename) == os.path.split(dirname):
            # We have reached the root component. Stop.
            components.append(dirname)
            break
        else:
            path = dirname

    components.reverse()

    return components
