Name:    hyperscan
Version: 5.2.1
Release: 1%{?dist}
Summary: High-performance regular expression matching library

License: BSD
URL:     https://www.hyperscan.io/
Source0: https://github.com/intel/%{name}/archive/v%{version}.tar.gz#/%{name}-%{version}.tar.gz
Source1: https://dl.bintray.com/boostorg/release/1.69.0/source/boost_1_69_0.tar.gz

BuildRequires:  gcc-c++
%if 0%{?rhel} >= 8 || 0%{?fedora}
BuildRequires:  boost-devel >= 1.57.0
%endif
BuildRequires:  cmake
BuildRequires:  pcre-devel
BuildRequires:  python3
BuildRequires:  ragel
BuildRequires:  sqlite-devel >= 3.0
BuildRequires:  libpcap-devel

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
%if 0%{?rhel} < 8
(cd include && tar zxf %{SOURCE1} boost_1_69_0/boost --strip-components=1)
%endif

%build
%cmake -DBUILD_SHARED_LIBS:BOOL=ON -DBUILD_STATIC_AND_SHARED:BOOL=OFF .
%make_build

%install
%make_install

%ldconfig_scriptlets

%files
%doc %{_defaultdocdir}/%{name}/examples/README.md
%doc %{_defaultdocdir}/%{name}/examples/*.cc
%doc %{_defaultdocdir}/%{name}/examples/*.c
%license COPYING
%license LICENSE
%{_libdir}/*.so.*

%files devel
%{_libdir}/*.so
%{_libdir}/pkgconfig/libhs.pc
%{_includedir}/hs/

%changelog
* Wed Oct 30 2019 Jason Taylor <jtfas90@gmail.com> - 5.2.1-1
- Latest upstream release

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 5.1.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Wed Apr 10 2019 Jason Taylor <jtfas90@gmail.com> - 5.1.1-1
- Latest upstream version (#1698365)
- Removed patch added for FTBFS (#1675120)

* Tue Feb 12 2019 Björn Esser <besser82@fedoraproject.org> - 5.1.0-1
- Latest upstream version (#1671192)
- Add patch to fix build (#1675120)

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 5.0.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 5.0.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Mon Jul 09 2018 Jason Taylor <jtfas90@gmail.com> - 5.0.0-1
- Latest upstream version

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 4.7.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Jan 25 2018 Jason Taylor <jtfas90@gmail.com> - 4.7.0-1
- upstream bugfix release

* Fri Sep 22 2017 Jason Taylor <jtfas90@gmail.com> - 4.6.0-1
- latest upstream release

* Wed Aug 02 2017 Fedora Release Engineering <releng@fedoraproject.org> - 4.5.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Thu Jul 27 2017 Jason Taylor <jtfas90@gmail.com> - 4.5.2-1
- upstream bugfix release

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 4.5.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Jun 16 2017 Jason Taylor <jtfas90@gmail.com> - 4.5.1-1
- upstream bugfix release

* Fri Jun 09 2017 Jason Taylor <jtfas90@gmail.com> - 4.5.0-1
- Update to latest upstream
- Removed CMakeLists.txt patch, moved into upstream

* Fri May 12 2017 Jason Taylor <jtfas90@gmail.com> - 4.4.1-1
- Update to latest upstream
- Add CMakeLists.txt path patch
- Spec file updates to meet packaging standards

* Fri Sep 2 2016 Jason Taylor <jtfas90@gmail.com> - 4.3.1-1
- Updated to latest upstream release.

* Fri Jul 1 2016 Jason Ish <ish@unx.ca> - 4.2.0-1
- Initial package of Hyperscan.
