# Spec file for package 'caf' and subpackages.
#
# Copyright (c) 2015, Pavel Kretov <firegurafiku@gmail.com>
#
# All modifications and additions to the file contributed by third parties
# remain the property of their copyright owners, unless otherwise agreed
# upon. The license for this file, and modifications and additions to the
# file, is the same license as for the pristine package itself (unless the
# license for the pristine package is not an Open Source License, in which
# case the license is the MIT License). An "Open Source License" is a
# license that conforms to the Open Source Definition (Version 1.9)
# published by the Open Source Initiative.

%define docdir %{_datadir}/doc/%{name}-%{version}
%if 0%{?fedora_version} == 20 || 0%{?fedora_version} == 21 || 0%{?suse_version} == 1310 || 0%{?suse_version} == 1320
%define supportsOpenCL 1
%endif

%define         dist_name actor-framework

Name:           caf
Version:        0.17.5
Release:        1%{?dist}
Summary:        C++ actor framework
License:        BSD
URL:            http://actor-framework.org
Source0:        https://github.com/actor-framework/%{dist_name}/archive/%{version}.tar.gz#/%{dist_name}-%{version}.tar.gz
Requires:       libcaf_core == %{version}
Requires:       libcaf_io   == %{version}
Requires:       libcaf_openssl == %{version}
BuildRequires:  cmake       >= 2.8
BuildRequires:  gcc-c++     >= 4.8
BuildRequires:  openssl-devel
BuildRequires:  python3-sphinx
BuildRequires:  python3-GitPython
%if 0%{?supportsOpenCL}
Requires:       libcaf_opencl == %{version}
BuildRequires:  opencl-headers
BuildRequires:  ocl-icd-devel
%endif

%description
CAF is an open source C++11 actor model implementation featuring
lightweight & fast actor implementations, pattern matching for messages,
network transparent messaging, and more.

%prep
%autosetup -S git -n %{dist_name}-%{version}

%build
mkdir build; cd build
%cmake -DCAF_NO_EXAMPLES:BOOL=yes ..
%make_build

cd ../manual
sphinx-build . html

%check
#make --directory=build test
ctest -V %{?_smp_mflags}

# By default CAF installs itself into /usr/lib, but some distros may use
# directories like /usr/lib64 or even /usr/lib32, the right location is
# expected to be held by "_libdir" macro. Unfortunately, there is no way
# for file directive to specify another target directory name, so we have
# to move library files into appropriate directory manually right after
# installation complete. Note that we run unit tests after that as we really
# do not want to ship broken package.
# Also note that we completely clean up old buildroot before installing, in
# order not to accidentaly pack old files left since previous build.
%install
rm -rf %{buildroot}
%make_install --directory=build

mkdir -p %{buildroot}/%{_docdir}/caf-doc/
cp -a manual/html %{buildroot}/%{_docdir}/caf-doc/

%clean
rm -rf %{buildroot}

# This section is empty as the master package does not really hold any files,
# leaving them to the subpackages.
%files

# ---- libcaf_core ----
%package -n libcaf_core
Summary:  C++ actor framework: core library
License:  BSD

%description -n libcaf_core
CAF is an open source C++11 actor model implementation featuring
lightweight & fast actor implementations, pattern matching for messages,
network transparent messaging, and more. This package contains the core
compiled library.

%files -n libcaf_core
%doc README*
%{_datadir}/caf/tools/

%license LICENSE*
%{_libdir}/libcaf_core.so.*

%post -n libcaf_core
/sbin/ldconfig

%postun -n libcaf_core
/sbin/ldconfig

# ---- libcaf_io ----
%package -n libcaf_io
Summary:  C++ actor framework: IO library
License:  BSD
Requires: libcaf_core == %{version}

%description -n libcaf_io
CAF is an open source C++11 actor model implementation featuring
lightweight & fast actor implementations, pattern matching for messages,
network transparent messaging, and more. This package contains the IO
compiled library.

%files -n libcaf_io
%doc README*
%license LICENSE*
%{_libdir}/libcaf_io.so.*

%post -n libcaf_io
/sbin/ldconfig

# ---- libcaf_openssl ----
%package -n libcaf_openssl
Summary:  C++ actor framework: OpenSSL library
License:  BSD
Requires: libcaf_core == %{version}

%description -n libcaf_openssl
CAF is an open source C++11 actor model implementation featuring
lightweight & fast actor implementations, pattern matching for messages,
network transparent messaging, and more. This package contains the OpenSSL
compiled library.

%files -n libcaf_openssl
%doc README*
%license LICENSE*
%{_libdir}/libcaf_openssl.so.*

%post -n libcaf_openssl
/sbin/ldconfig

%postun -n libcaf_openssl
/sbin/ldconfig

# ---- libcaf_opencl ----
%if 0%{?supportsOpenCL}
%package -n libcaf_opencl
Summary:  C++ actor framework: OpenCL support library
License:  BSD
Requires: libcaf_core == %{version}

%description -n libcaf_opencl
CAF is an open source C++11 actor model implementation featuring
lightweight & fast actor implementations, pattern matching for messages,
network transparent messaging, and more. This package contains the OpenCL
compiled library.

%files -n libcaf_opencl
%doc README*
%license LICENSE*
%{_libdir}/libcaf_opencl.so.*

%post -n libcaf_opencl
/sbin/ldconfig

%postun -n libcaf_opencl
/sbin/ldconfig
%endif

# ---- caf-devel ----
%package  devel
Summary:  C++ actor framework: header files
License:  BSD
Requires: caf == %{version}

%description devel
C++ header files for all "libcaf_*" packages for application development using
CAF. This package will also install all of them.

%files devel
%doc README*
%license LICENSE*
/usr/include/caf/
%{_libdir}/libcaf_*.so

# ---- caf-doc ----
%package doc
Summary:  C++ actor framework: documentation in HTML format
License:  BSD
Requires: caf == %{version}


%description doc
This package includes documentation for CAF developer, available in HTML or
plain text format. This includes README and LICENSE files, reference
documentation, generated by Doxygen, and current version of programmer's
manual.

%files doc
%doc README*
%license LICENSE*
%{_docdir}/caf-doc/

%changelog
* Tue May 19 2020 Derek Ditch <derek@rocknsm.io> 0.17.5-1
- Bump version to 0.17.5 to fix doc builds w/ python3
- Explicitly build with python3-devel

* Mon Dec 16 2019 Derek Ditch <derek@rocknsm.io> 0.17.3-1
- Version bump to latest upstream release

* Mon Sep 16 2019 Derek Ditch <derek@rocknsm.io> 0.17.1-1
- Version bump to latest build
- Patch install dirs to use CMAKE_INSTALL_* vars

* Wed Feb 6 2019 Derek Ditch <derek@rocksnm.io> 0.16.3-1
- Package for EL7 and RockNSM

* Mon Jun 1 2015 Pavel Kretov <firegurafiku@gmail.com> 0.13.2
- First packaged version.
