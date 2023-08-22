"""Utilities for extracting common archive formats"""

import zipfile
import tarfile
import os
import shutil
import posixpath
import contextlib
from distutils.errors import DistutilsError

from ._path import ensure_directory

__all__ = [
<<<<<<< HEAD
    "unpack_archive", "unpack_zipfile", "unpack_tarfile", "default_filter",
    "UnrecognizedFormat", "extraction_drivers", "unpack_directory",
=======
    "unpack_archive",
    "unpack_zipfile",
    "unpack_tarfile",
    "default_filter",
    "UnrecognizedFormat",
    "extraction_drivers",
    "unpack_directory",
>>>>>>> 72864d1 (Tue 22 Aug 2023 02:44:06 PM CDT)
]


class UnrecognizedFormat(DistutilsError):
    """Couldn't recognize the archive type"""


def default_filter(src, dst):
    """The default progress/filter callback; returns True for all files"""
    return dst


<<<<<<< HEAD
def unpack_archive(
        filename, extract_dir, progress_filter=default_filter,
        drivers=None):
=======
def unpack_archive(filename, extract_dir, progress_filter=default_filter, drivers=None):
>>>>>>> 72864d1 (Tue 22 Aug 2023 02:44:06 PM CDT)
    """Unpack `filename` to `extract_dir`, or raise ``UnrecognizedFormat``

    `progress_filter` is a function taking two arguments: a source path
    internal to the archive ('/'-separated), and a filesystem path where it
    will be extracted.  The callback must return the desired extract path
    (which may be the same as the one passed in), or else ``None`` to skip
    that file or directory.  The callback can thus be used to report on the
    progress of the extraction, as well as to filter the items extracted or
    alter their extraction paths.

    `drivers`, if supplied, must be a non-empty sequence of functions with the
    same signature as this function (minus the `drivers` argument), that raise
    ``UnrecognizedFormat`` if they do not support extracting the designated
    archive type.  The `drivers` are tried in sequence until one is found that
    does not raise an error, or until all are exhausted (in which case
    ``UnrecognizedFormat`` is raised).  If you do not supply a sequence of
    drivers, the module's ``extraction_drivers`` constant will be used, which
    means that ``unpack_zipfile`` and ``unpack_tarfile`` will be tried, in that
    order.
    """
    for driver in drivers or extraction_drivers:
        try:
            driver(filename, extract_dir, progress_filter)
        except UnrecognizedFormat:
            continue
        else:
            return
    else:
<<<<<<< HEAD
        raise UnrecognizedFormat(
            "Not a recognized archive type: %s" % filename
        )


def unpack_directory(filename, extract_dir, progress_filter=default_filter):
    """"Unpack" a directory, using the same interface as for archives
=======
        raise UnrecognizedFormat("Not a recognized archive type: %s" % filename)


def unpack_directory(filename, extract_dir, progress_filter=default_filter):
    """ "Unpack" a directory, using the same interface as for archives
>>>>>>> 72864d1 (Tue 22 Aug 2023 02:44:06 PM CDT)

    Raises ``UnrecognizedFormat`` if `filename` is not a directory
    """
    if not os.path.isdir(filename):
        raise UnrecognizedFormat("%s is not a directory" % filename)

    paths = {
        filename: ('', extract_dir),
    }
    for base, dirs, files in os.walk(filename):
        src, dst = paths[base]
        for d in dirs:
            paths[os.path.join(base, d)] = src + d + '/', os.path.join(dst, d)
        for f in files:
            target = os.path.join(dst, f)
            target = progress_filter(src + f, target)
            if not target:
                # skip non-files
                continue
            ensure_directory(target)
            f = os.path.join(base, f)
            shutil.copyfile(f, target)
            shutil.copystat(f, target)


def unpack_zipfile(filename, extract_dir, progress_filter=default_filter):
    """Unpack zip `filename` to `extract_dir`

    Raises ``UnrecognizedFormat`` if `filename` is not a zipfile (as determined
    by ``zipfile.is_zipfile()``).  See ``unpack_archive()`` for an explanation
    of the `progress_filter` argument.
    """

    if not zipfile.is_zipfile(filename):
        raise UnrecognizedFormat("%s is not a zip file" % (filename,))

    with zipfile.ZipFile(filename) as z:
        _unpack_zipfile_obj(z, extract_dir, progress_filter)


def _unpack_zipfile_obj(zipfile_obj, extract_dir, progress_filter=default_filter):
    """Internal/private API used by other parts of setuptools.
    Similar to ``unpack_zipfile``, but receives an already opened :obj:`zipfile.ZipFile`
    object instead of a filename.
    """
    for info in zipfile_obj.infolist():
        name = info.filename

        # don't extract absolute paths or ones with .. in them
        if name.startswith('/') or '..' in name.split('/'):
            continue

        target = os.path.join(extract_dir, *name.split('/'))
        target = progress_filter(name, target)
        if not target:
            continue
        if name.endswith('/'):
            # directory
            ensure_directory(target)
        else:
            # file
            ensure_directory(target)
            data = zipfile_obj.read(info.filename)
            with open(target, 'wb') as f:
                f.write(data)
        unix_attributes = info.external_attr >> 16
        if unix_attributes:
            os.chmod(target, unix_attributes)


def _resolve_tar_file_or_dir(tar_obj, tar_member_obj):
    """Resolve any links and extract link targets as normal files."""
    while tar_member_obj is not None and (
<<<<<<< HEAD
            tar_member_obj.islnk() or tar_member_obj.issym()):
=======
        tar_member_obj.islnk() or tar_member_obj.issym()
    ):
>>>>>>> 72864d1 (Tue 22 Aug 2023 02:44:06 PM CDT)
        linkpath = tar_member_obj.linkname
        if tar_member_obj.issym():
            base = posixpath.dirname(tar_member_obj.name)
            linkpath = posixpath.join(base, linkpath)
            linkpath = posixpath.normpath(linkpath)
        tar_member_obj = tar_obj._getmember(linkpath)

<<<<<<< HEAD
    is_file_or_dir = (
        tar_member_obj is not None and
        (tar_member_obj.isfile() or tar_member_obj.isdir())
=======
    is_file_or_dir = tar_member_obj is not None and (
        tar_member_obj.isfile() or tar_member_obj.isdir()
>>>>>>> 72864d1 (Tue 22 Aug 2023 02:44:06 PM CDT)
    )
    if is_file_or_dir:
        return tar_member_obj

    raise LookupError('Got unknown file type')


def _iter_open_tar(tar_obj, extract_dir, progress_filter):
    """Emit member-destination pairs from a tar archive."""
    # don't do any chowning!
    tar_obj.chown = lambda *args: None

    with contextlib.closing(tar_obj):
        for member in tar_obj:
            name = member.name
            # don't extract absolute paths or ones with .. in them
            if name.startswith('/') or '..' in name.split('/'):
                continue

            prelim_dst = os.path.join(extract_dir, *name.split('/'))

            try:
                member = _resolve_tar_file_or_dir(tar_obj, member)
            except LookupError:
                continue

            final_dst = progress_filter(name, prelim_dst)
            if not final_dst:
                continue

            if final_dst.endswith(os.sep):
                final_dst = final_dst[:-1]

            yield member, final_dst


def unpack_tarfile(filename, extract_dir, progress_filter=default_filter):
    """Unpack tar/tar.gz/tar.bz2 `filename` to `extract_dir`

    Raises ``UnrecognizedFormat`` if `filename` is not a tarfile (as determined
    by ``tarfile.open()``).  See ``unpack_archive()`` for an explanation
    of the `progress_filter` argument.
    """
    try:
        tarobj = tarfile.open(filename)
    except tarfile.TarError as e:
        raise UnrecognizedFormat(
            "%s is not a compressed or uncompressed tar file" % (filename,)
        ) from e

    for member, final_dst in _iter_open_tar(
<<<<<<< HEAD
            tarobj, extract_dir, progress_filter,
=======
        tarobj,
        extract_dir,
        progress_filter,
>>>>>>> 72864d1 (Tue 22 Aug 2023 02:44:06 PM CDT)
    ):
        try:
            # XXX Ugh
            tarobj._extract_member(member, final_dst)
        except tarfile.ExtractError:
            # chown/chmod/mkfifo/mknode/makedev failed
            pass

    return True


extraction_drivers = unpack_directory, unpack_zipfile, unpack_tarfile
