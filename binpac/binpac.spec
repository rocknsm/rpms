Name:           binpac
Version:        0.53
Release:        1%{?dist}
Epoch:          1
Summary:        High level language for describing protocol parsers.

License:        BSD
URL:            https://github.com/zeek/binpac
Source0:        https://www.zeek.org/downloads/%{name}-%{version}.tar.gz
Patch0:         https://github.com/zeek/binpac/commit/5ffea9d9ba2f1b04b3cdc11225eea71ee41894a5.patch#/fix-gnu-install-dirs.patch
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  cmake >= 2.8.12
BuildRequires:  flex
BuildRequires:  bison
BuildRequires:  gcc-c++

%description
BinPAC is a high level language for describing protocol parsers and
generates C++ code.  It is currently maintained and distributed with the
Bro Network Security Monitor distribution, however, the generated parsers
may be used with other programs besides Bro.

%package devel
Summary: Development headers and static library for binpac

%description devel
BinPAC is a high level language for describing protocol parsers and
generates C++ code.  It is currently maintained and distributed with the
Bro Network Security Monitor distribution, however, the generated parsers
may be used with other programs besides Bro.

This package contains the development headers and static library.

%prep
%setup -q
%patch0 -p1

%build
mkdir build; cd build
%cmake .. -DENABLE_STATIC=true
make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%doc README
%doc CHANGES
%license COPYING
/usr/bin/binpac

%files devel
%{_includedir}/binpac*
%{_libdir}/libbinpac.a

%changelog
* Fri Aug 23 2019 Derek Ditch <derek@rocknsm.io> 0.53-1
- Bump version to 0.53

* Wed Feb 13 2019 Derek Ditch <derek@rocknsm.io> 0.51-1
- Initial RPM packaging
