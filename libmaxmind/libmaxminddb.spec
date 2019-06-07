#
# spec file for package libmaxminddb
#
# Copyright (c) 2016 SUSE LINUX Products GmbH, Nuernberg, Germany.
#
# All modifications and additions to the file contributed by third parties
# remain the property of their copyright owners, unless otherwise agreed
# upon. The license for this file, and modifications and additions to the
# file, is the same license as for the pristine package itself (unless the
# license for the pristine package is not an Open Source License, in which
# case the license is the MIT License). An "Open Source License" is a
# license that conforms to the Open Source Definition (Version 1.9)
# published by the Open Source Initiative.

# Please submit bugfixes or comments via http://bugs.opensuse.org/
#


Name:           libmaxminddb
%define lname   libmaxminddb0
Version:        1.3.2
Release:        1%{dist}
Summary:        C library for the MaxMind DB file format
License:        Apache-2.0
Group:          Development/Libraries/C and C++
Source:         https://github.com/maxmind/libmaxminddb/releases/download/%{version}/%{name}-%{version}.tar.gz
Url:            http://dev.maxmind.com/
BuildRequires:  fdupes
BuildRequires:  gcc-c++
BuildRequires:  pkgconfig
BuildRoot:      %{_tmppath}/%{name}-%{version}-build

%description
The libmaxminddb library provides a C library for reading MaxMind DB
files, including the GeoIP2 databases from MaxMind. This is a
custom binary format designed to facilitate fast lookups of IP
addresses while allowing for great flexibility in the type of
data associated with an address.

%package -n %lname
Summary:        C library for the MaxMind DB file format
Group:          System/Libraries

%description -n %lname
The libmaxminddb library provides a C library for reading MaxMind DB
files, including the GeoIP2 databases from MaxMind. This is a
custom binary format designed to facilitate fast lookups of IP
addresses while allowing for great flexibility in the type of
data associated with an address.

%package -n mmdblookup
Summary:        An utility to look up an IP address in a MaxMind DB file
Group:          Productivity/Networking/Other

%description -n mmdblookup
The libmaxminddb library provides a C library for reading MaxMind DB
files, including the GeoIP2 databases from MaxMind. This is a
custom binary format designed to facilitate fast lookups of IP
addresses while allowing for great flexibility in the type of
data associated with an address.

This package contains the mmdblookup binary.

%package devel
Summary:        Development files for the MaxMind DB file format library
Group:          Development/Libraries/C and C++
Requires:       %lname = %version

%description devel
The libmaxminddb library provides a C library for reading MaxMind DB
files, including the GeoIP2 databases from MaxMind. This is a
custom binary format designed to facilitate fast lookups of IP
addresses while allowing for great flexibility in the type of
data associated with an address.

This package contains the development files for %{name}.

%prep
%setup -q

%build
%configure --disable-static
make %{?_smp_mflags}

%install
%make_install
rm %buildroot/%_libdir/*.la
%fdupes -s %buildroot/%_prefix

%post   -n %lname -p /sbin/ldconfig
%postun -n %lname -p /sbin/ldconfig

%files -n %lname
%defattr(-,root,root)
%doc LICENSE
%{_libdir}/%{name}.so.*

%files -n mmdblookup
%defattr(-,root,root)
%doc doc/mmdblookup.md
%{_bindir}/mmdblookup
%{_mandir}/man1/mmdblookup.*

%files devel
%defattr(-,root,root)
%doc Changes.md NOTICE README.md doc/mmdblookup.md doc/libmaxminddb.md
%{_includedir}/*
%{_libdir}/%{name}.so
%{_libdir}/pkgconfig/%{name}.pc
%{_mandir}/man3/%{name}.*
%{_mandir}/man3/MMDB_*.*

%changelog
* Mon Feb 11 2018 Derek Ditch <derek@rocknsm.io> 1.3.2-1
- Update to version 1.3.2
* Tue Apr 12 2016 p.drouand@gmail.com
- Update to version 1.2.0
  * Four additional fields were added to the end of the
    MMDB_search_node_s struct returned by MMDB_read_node. These
    fields allow the user to iterate through the search tree without
    making undocumented assumptions about how this library works
    internally and without knowing the specific details of the database
    format. GitHub #110 (https://github.com/maxmind/libmaxminddb/issues/110)
- Changes from version 1.1.5
  * Previously, reading a database with a pointer in the metadata would
    cause an MMDB_INVALID_METADATA_ERROR to be returned. This was due to
    an invalid offset being used when calculating the pointer. The
    data_section and metadata_section fields now both point to the
    beginning of the data section. Previously, data_section pointed
    to the beginning of the data separator. This will not affect
    anyone using only documented fields from MMDB_s.
  * MMDB_lookup_sockaddr will set mmdb_error to
    MMDB_IPV6_LOOKUP_IN_IPV4_DATABASE_ERROR if an IPv6 sockaddr is
    looked up in an IPv4-only database. Previously only
    MMDB_lookup_string would set this error code.
  * When resolving an address, this library now relies on getaddrinfo
    to determine the address family rather than trying to guess it itself.
- Changes from version 1.1.4
  * Packaging fixes. The 1.1.3 tarball release contained a lot of extra
    junk in the t/ directory.
- Changes from version 1.1.3
  * Added several additional checks to make sure that we don't attempt to read
    past the end of the databases's data section. GitHub #103
    (https://github.com/maxmind/libmaxminddb/pull/103).
  * When searching for the database metadata, there was a bug that caused
    the code to think it had found valid metadata when none existed. In
    addition, this could lead to an attempt to read past the end of the
    database entirely. Finally, if there are multiple metadata markers
    in the database, we treat the final one as the start of the metdata,
    instead of the first. GitHub #102 (https://github.com/maxmind/libmaxminddb/pull/102)
  * Don't attempt to mmap a file that is too large to be mmapped on the system.
    GitHub #101 (https://github.com/maxmind/libmaxminddb/pull/101).
  * Added a missing out of memory check when reading a file's metadata.
    GitHub #101 (https://github.com/maxmind/libmaxminddb/pull/101).
  * Added several additional checks to make sure that we never attempt
    to malloc more than SIZE_MAX memory, which would lead to integer
    overflow. This could only happen with pathological databases.
    GitHub #101 (https://github.com/maxmind/libmaxminddb/pull/101).
* Wed Nov 18 2015 p.drouand@gmail.com
- Update to version 1.1.2
  * IMPORTANT: This release includes a number of important security
    fixes. Among these fixes is improved validation of the database
    metadata. Unfortunately, MaxMind GeoIP2 and GeoLite2 databases
    created earlier than January 28, 2014, had an invalid data type
    for the record_size in the metadata. Previously these databases
    worked on little endian machines with libmaxminddb but did not
    work on big endian machines. Due to increased safety checks when
    reading the file, these databases will no longer work on any
    platform. If you are using one of these databases, we recommend
    that you upgrade to the latest GeoLite2 or GeoIP2 database
  * Added pkg-config support.
  * Several segmentation faults found with afl-fuzz were fixed. These
    were caused by missing bounds checking and missing verification
    of data type.
    MMDB_get_entry_data_list will now fail on data structures with a
    depth greater than 512 and data structures that are cyclic. This
    should not affect any known MaxMind DB in production. All databases
    produced by MaxMind have a depth of less than five.
- Add a build dependency to pkg-config
* Sun Jul 26 2015 p.drouand@gmail.com
- Update to version 1.1.1
  * Added `maxminddb-compat-util.h` as a source file to dist.
- Changes from version 1.1.0
  * Previously, when there was an error in `MMDB_open()`, `errno` would
    generally be overwritten during cleanup, preventing a useful value from
    being returned to the caller. This was changed so that the `errno` value
    from the function call that caused the error is restored before returning to
    the caller. In particular, this is important for `MMDB_IO_ERROR` errors as
    checking `errno` is often the only way to determine what actually failed.
  * If `mmap()` fails due to running out of memory space, an
    `MMDB_OUT_OF_MEMORY_ERROR` is now returned from `MMDB_open` rather than an
    `MMDB_IO_ERROR`.
  * On Windows, the `CreateFileMappingA()` handle was not properly closed if
    opening the database succeeded. Fixed by Bly Hostetler. GitHub #75 & #76.
  * On Windows, we were not checking the return value of `CreateFileMappingA()`
    properly for errors. Fixed by Bly Hotetler. GitHub #78.
  * Several warnings from Clang's scan-build were fixed. GitHub #86.
  * All headers are now installed in `$(includedir)`. GitHub #89.
  * We no longer install `maxminddb-compat-util.h`. This header was intended for
    internal use only.
* Wed Jan 21 2015 p.drouand@gmail.com
- Update to version 1.0.4
  * If you used a non-integer string as an array index when doing a
    lookup with MMDB_get_value, MMDB_vget_value, or MMDB_aget_value,
    the first element of the array would be returned rather than an
    error. A MMDB_LOOKUP_PATH_DOES_NOT_MATCH_DATA_ERROR error will
    now be returned. GitHub #61.
  * If a number larger than LONG_MAX was used in the same functions,
    LONG_MAX would have been used in the lookup. Now a
    MMDB_INVALID_LOOKUP_PATH_ERROR error will be returned.
  * Visual Studio build files were added for unit tests and some
    compatibility issues with the tests were fixed.
  * Visual Studio project was updated to use property pages. GitHub #69.
  * A test failure in t/compile_c++_t.pl on new installs was fixed.
* Sun Dec 21 2014 p.drouand@gmail.com
- Initial release (version 1.0.3)
