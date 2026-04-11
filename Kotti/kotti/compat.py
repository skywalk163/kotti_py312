"""
Compatibility module for Python 3.12+.

This module provides replacements for deprecated/removed modules.
"""
from __future__ import annotations

import io
import sys
from typing import Any, BinaryIO, Optional

if sys.version_info >= (3, 9):
    from importlib.resources import files, as_file
    from importlib.metadata import version, PackageNotFoundError
else:
    from importlib_resources import files, as_file
    from importlib_metadata import version, PackageNotFoundError


def get_distribution_version(package_name: str) -> Optional[str]:
    """Get the version of an installed package.

    Replacement for pkg_resources.require(package_name)[0].version

    Args:
        package_name: The name of the package.

    Returns:
        The version string, or None if the package is not found.
    """
    try:
        return version(package_name)
    except PackageNotFoundError:
        return None


def get_resource_filename(package: str, resource: str) -> str:
    """Get the filesystem path to a package resource.

    Replacement for pkg_resources.resource_filename(package, resource).

    Args:
        package: The package name (e.g., 'kotti').
        resource: The resource path relative to the package.

    Returns:
        The filesystem path to the resource.
    """
    # For resources that need to be actual files (not in a zip)
    resource_files = files(package) / resource
    with as_file(resource_files) as path:
        return str(path)


def get_resource_path(package: str) -> str:
    """Get the filesystem path to a package directory.

    Replacement for pkg_resources.resource_filename(package, '').

    Args:
        package: The package name (e.g., 'kotti').

    Returns:
        The filesystem path to the package directory.
    """
    package_files = files(package)
    with as_file(package_files) as path:
        return str(path)


class FieldStorage:
    """Replacement for cgi.FieldStorage which was removed in Python 3.12.

    This is a minimal implementation that provides the attributes
    needed by Kotti's file upload handling.

    Attributes:
        file: A file-like object containing the uploaded data.
        filename: The original filename of the uploaded file.
        type: The MIME type of the uploaded file.
        length: The size of the uploaded file in bytes.
    """

    def __init__(
        self,
        fp: Optional[BinaryIO] = None,
        filename: Optional[str] = None,
        mimetype: Optional[str] = None,
        size: Optional[int] = None,
    ):
        self.file: Optional[BinaryIO] = fp
        self.filename: Optional[str] = filename
        self.type: Optional[str] = mimetype
        self.length: Optional[int] = size
        self.name: Optional[str] = None
        self.list: Optional[list] = None
        self.headers: dict = {}

    @property
    def value(self) -> bytes:
        """Return the file contents as bytes."""
        if self.file is None:
            return b""
        pos = self.file.tell()
        self.file.seek(0)
        data = self.file.read()
        self.file.seek(pos)
        return data

    def read(self, size: int = -1) -> bytes:
        """Read from the file."""
        if self.file is None:
            return b""
        return self.file.read(size)

    def readline(self) -> bytes:
        """Read a line from the file."""
        if self.file is None:
            return b""
        return self.file.readline()

    def readlines(self) -> list[bytes]:
        """Read all lines from the file."""
        if self.file is None:
            return []
        return self.file.readlines()

    def seek(self, offset: int, whence: int = 0) -> None:
        """Seek to a position in the file."""
        if self.file is not None:
            self.file.seek(offset, whence)

    def tell(self) -> int:
        """Return the current file position."""
        if self.file is None:
            return 0
        return self.file.tell()

    def __repr__(self) -> str:
        return f"<FieldStorage({self.filename!r}, {self.type!r})>"


def _to_fieldstorage(
    fp: BinaryIO,
    filename: str,
    mimetype: str,
    size: int,
    **kwds: Any,
) -> FieldStorage:
    """Build a FieldStorage instance.

    Deform's FileUploadWidget returns a dict, but
    depot.fields.sqlalchemy.UploadedFileField likes
    FieldStorage objects.

    Args:
        fp: File pointer to the uploaded data.
        filename: Original filename.
        mimetype: MIME type of the file.
        size: Size of the file in bytes.

    Returns:
        A FieldStorage instance.
    """
    return FieldStorage(fp=fp, filename=filename, mimetype=mimetype, size=size)
