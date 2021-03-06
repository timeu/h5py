.. _file:


HDF5 File Objects
=================

File objects serve as your entry point into the world of HDF5.  In addition
to the File-specific capabilities listed here, every File instance is
also an :ref:`HDF5 group <group>` representing the `root group` of the file.

.. _file_open:

Opening & creating files
------------------------

HDF5 files work generally like standard Python file objects.  They support
standard modes like r/w/a, and should be closed when they are no longer in
use.  However, there is obviously no concept of "text" vs "binary" mode.

    >>> f = h5py.File('myfile.hdf5','r')

The file name may be a byte string or unicode string. Valid modes are:

    ===  ================================================
     r   Readonly, file must exist
     r+  Read/write, file must exist
     w   Create file, truncate if exists
     w-  Create file, fail if exists
     a   Read/write if exists, create otherwise (default)
    ===  ================================================


.. _file_driver:

File drivers
------------

HDF5 ships with a variety of different low-level drivers, which map the logical
HDF5 address space to different storage mechanisms.  You can specify which
driver you want to use when the file is opened::

    >>> f = h5py.File('myfile.hdf5', driver=<driver name>, <driver_kwds>)

For example, the HDF5 "core" driver can be used to create a purely in-memory
HDF5 file, optionally written out to disk when it is closed.  Here's a list
of supported drivers and their options:

    None
        **Strongly recommended.** Use the standard HDF5 driver appropriate
        for the current platform. On UNIX, this is the H5FD_SEC2 driver;
        on Windows, it is H5FD_WINDOWS.

    'sec2'
        Unbuffered, optimized I/O using standard POSIX functions.

    'stdio' 
        Buffered I/O using functions from stdio.h.

    'core'
        Memory-map the entire file; all operations are performed in
        memory and written back out when the file is closed.  Keywords:

        backing_store:  If True (default), save changes to a real file
                        when closing.  If False, the file exists purely
                        in memory and is discarded when closed.

        block_size:     Increment (in bytes) by which memory is extended.
                        Default is 64k.

    'family'
        Store the file on disk as a series of fixed-length chunks.  Useful
        if the file system doesn't allow large files.  Note: the filename
        you provide *must* contain a printf-style integer format code
        (e.g. %d"), which will be replaced by the file sequence number.
        Keywords:

        memb_size:  Maximum file size (default is 2**31-1).


.. _file_version:

Version Bounding
----------------

HDF5 has been evolving for many years now.  By default, the library will
write objects in the most compatible fashion possible, so that older versions
will still be able to read files generated by modern programs.  However, there
can be performance advantages if you are willing to forgo a certain level
of backwards compatibility.  By using the "libver" option to File, you can
specify the minimum and maximum sophistication of these structures:

    >>> f = h5py.File('name.hdf5', libver='earliest') # most compatible
    >>> f = h5py.File('name.hdf5', libver='latest')   # most modern

Here "latest" means that HDF5 will always use the newest version of these
structures without particular concern for backwards compatibility.  The
"earliest" option means that HDF5 will make a *best effort* to be backwards
compatible.

The default is "earliest".


.. _file_userblock:

User block
----------

HDF5 allows the user to insert arbitrary data at the beginning of the file,
in a reserved space called the `user block`.  The length of the user block
must be specified when the file is created.  It can be either zero
(the default) or a power of two greater than or equal to 512.  You
can specify the size of the user block when creating a new file, via the
``userblock_size`` keyword to File; the userblock size of an open file can
likewise be queried through the ``File.userblock_size`` property.

Modifying the user block on an open file is not supported; this is a limitation
of the HDF5 library.  However, once the file is closed you are free to read and
write data at the start of the file, provided your modifications don't leave
the user block region.

Reference
---------

.. note::
    
    Unlike Python file objects, the attribute ``File.name`` gives the
    HDF5 name of the root group, "``/``". To access the on-disk name, use
    :attr:`File.filename`.

.. class:: File(name, mode=None, driver=None, libver=None, userblock_size, **kwds)

    Open or create a new file.

    Note that in addition to the File-specific methods and properties listed
    below, File objects inherit the full interface of :class:`Group`.

    :param name:    Name of file (`str` or `unicode`), or an instance of
                    :class:`h5f.FileID` to bind to an existing
                    file identifier.
    :param mode:    Mode in which to open file; one of
                    ("w", "r", "r+", "a", "w-").  See :ref:`file_open`.
    :param driver:  File driver to use; see :ref:`file_driver`.
    :param libver:  Compatibility bounds; see :ref:`file_version`.
    :param userblock_size:  Size (in bytes) of the user block.  If nonzero,
                    must be a power of 2 and at least 512.  See
                    :ref:`file_userblock`.
    :param kwds:    Driver-specific keywords; see :ref:`file_driver`.

    .. method:: close()

        Close this file.  All open objects will become invalid.

    .. method:: flush()

        Request that the HDF5 library flush its buffers to disk.

    .. attribute:: id

        Low-level identifier (an instance of :class:`FileID <low:h5py.h5f.FileID>`).

    .. attribute:: filename

        Name of this file on disk.  Generally a Unicode string; a byte string
        will be used if HDF5 returns a non-UTF-8 encoded string.

    .. attribute:: mode

        String indicating if the file is open readonly ("r") or read-write
        ("r+").  Will always be one of these two values, regardless of the
        mode used to open the file.

    .. attribute:: driver

        String giving the driver used to open the file.  Refer to
        :ref:`file_driver` for a list of drivers.

    .. attribute:: libver

        2-tuple with library version settings.  See :ref:`file_version`.

    .. attribute:: userblock_size

        Size of user block (in bytes).  Generally 0.  See :ref:`file_userblock`.