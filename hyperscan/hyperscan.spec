Name:    hyperscan
Version: 5.1.0
Release: 1%{?dist}
Summary: High-performance regular expression matching library

License: BSD
URL:     https://www.hyperscan.io/
Source0: https://github.com/intel/%{name}/archive/v%{version}.tar.gz#/%{name}-%{version}.tar.gz
Source1: https://dl.bintray.com/boostorg/release/1.66.0/source/boost_1_66_0.tar.gz

%if 0%{?rhel} < 8
BuildRequires:    cmake3  >= 3.0.0
%global cmake %cmake3
%global ctest /usr/bin/ctest3
%else
BuildRequires:    cmake   >= 3.0.0
%global ctest /usr/bin/ctest
%endif 

BuildRequires:  pcre-devel
BuildRequires:  python3-devel
BuildRequires:  ragel
BuildRequires:  sqlite-devel
BuildRequires:  libpcap-devel
BuildRequires:  gcc-c++

Requires:	pcre
Requires:	sqlite

#package requires SSE support and fails to build on non x86_64 archs
ExclusiveArch: x86_64

%description
Hyperscan is a high-performance multiple regex matching library. It
follows the regular expression syntax of the commonly-used libpcre
library, but is a standalone library with its own C API.

Hyperscan uses hybrid automata techniques to allow simultaneous
matching of large numbers (up to tens of thousands) of regular
expressions and for the matching of regular expressions across streams
of data.

Hyperscan is typically used in a DPI library stack.

%package static
Summary: Static library library files for the hyperscan library
Provides: %{name}%{?_isa}

%description static
Hyperscan is a high-performance multiple regex matching library. It
follows the regular expression syntax of the commonly-used libpcre
library, but is a standalone library with its own C API.

Hyperscan uses hybrid automata techniques to allow simultaneous
matching of large numbers (up to tens of thousands) of regular
expressions and for the matching of regular expressions across streams
of data.

Hyperscan is typically used in a DPI library stack.

This package provides static library files for the hyperscan library.

%package devel
Summary: Libraries and header files for the hyperscan library
Requires: %{name}%{?_isa} = %{version}-%{release}

%description devel
Hyperscan is a high-performance multiple regex matching library. It
follows the regular expression syntax of the commonly-used libpcre
library, but is a standalone library with its own C API.

Hyperscan uses hybrid automata techniques to allow simultaneous
matching of large numbers (up to tens of thousands) of regular
expressions and for the matching of regular expressions across streams
of data.

Hyperscan is typically used in a DPI library stack.

This package provides the libraries, include files and other resources
needed for developing Hyperscan applications.

%prep
%autosetup
(cd include && tar zxf %{SOURCE1} boost_1_66_0/boost --strip-components=1)

%build
%cmake -DBUILD_SHARED_LIBS:BOOL=OFF -DBUILD_STATIC_AND_SHARED:BOOL=ON \
       -DCMAKE_POSITION_INDEPENDENT_CODE:BOOL=true .

%make_build

%install
make install DESTDIR=%{buildroot}
cp lib/libhs.a %{buildroot}%{_libdir}

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%doc %{_defaultdocdir}/%{name}/examples/README.md
%doc %{_defaultdocdir}/%{name}/examples/*.cc
%doc %{_defaultdocdir}/%{name}/examples/*.c
%license COPYING
%license LICENSE
%{_libdir}/*.so.*
%{_libdir}/*.so

%files static
%{_libdir}/*.a

%files devel
%{_libdir}/pkgconfig/libhs.pc
%{_includedir}/hs/

%changelog
* Mon Feb 11 2019 Derek Ditch <derek@rocknsm.io> - 5.1.0-1
- update version to 5.1.0

* Tue Oct 02 2018 Jason Taylor <jtfas90@gmail.com> - 5.0.0-1
- update version to 5.0.0
- update bundled boost to 1.66.0
- updated links

* Wed Feb  7 2018 Jason Ish <ish@unx.ca> - 4.7.0-1
- Update to 4.7.0.

* Thu Jan  4 2018 Jason Ish <ish@unx.ca> - 4.6.0-1
- Update to v4.6.0.

* Thu Jul 27 2017 Jason Ish <ish@unx.ca> - 4.5.2-1
- Update to 4.5.2.

* Thu Jul 27 2017 Jason Ish <ish@unx.ca> - 4.5.1-2
- Break out the static libs into their own package.

* Wed Jun 28 2017 Jason Ish <ish@unx.ca> - 4.4.1-2
- Include static library.

* Fri Jun 16 2017 Jason Taylor <jtfas90@gmail.com> - 4.5.1-1
- upstream bugfix release

* Fri Jun 09 2017 Jason Taylor <jtfas90@gmail.com> - 4.5.0-1
- Update to latest upstream
- Removed CMakeLists.txt patch, moved into upstream

* Fri May 12 2017 Jason Taylor <jtfas90@gmail.com> - 4.4.1-1
- Update to latest upstream
- Add CMakeLists.txt path patch
- Spec file updates to meet packaging standards

* Mon Jan 30 2017 Jason Ish <ish@unx.ca> - 4.4.0-1
- Update to 4.4.0.

* Fri Sep 2 2016 Jason Taylor <jtfas90@gmail.com> - 4.3.1-1
- Updated to latest upstream release.

* Fri Jul 1 2016 Jason Ish <ish@unx.ca> - 4.2.0-1
- Initial package of Hyperscan.
