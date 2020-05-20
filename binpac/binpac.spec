%if 0%{?rhel} < 8
%global scl devtoolset-8
%global scl_prefix devtoolset-8-
%global scl_enable cat << EOSCL | scl enable %{scl} -
%global scl_disable EOSCL
%endif

Name:           binpac
Version:        0.55.1
Release:        1%{?dist}
Epoch:          1
Summary:        High level language for describing protocol parsers.

License:        BSD
URL:            https://github.com/zeek/binpac
Source0:        https://download.zeek.org/%{name}-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

%if 0%{?rhel} < 8
BuildRequires:    cmake3  >= 3.0.0
%global cmake %cmake3
%else
BuildRequires:    cmake   >= 3.0.0
%endif 
BuildRequires:  flex
BuildRequires:  bison
BuildRequires:  %{?scl_prefix}gcc-c++ >= 8

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
%autosetup -p1

%build
mkdir build; cd build
%{?scl_enable} 
%cmake .. -DENABLE_STATIC=true
make %{?_smp_mflags}
%{?scl_disable}

%install
rm -rf $RPM_BUILD_ROOT
%{?scl_enable} 
make install DESTDIR=$RPM_BUILD_ROOT
%{?scl_disable}

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
%{_libdir}/libbinpac.so*

%changelog
* Wed May 20 2020 Derek Ditch <derek@rocknsm.io> 0.55.1-1
- Bump version to 0.55.1 or Zeek 3.1.x
- Use cmake3 and g++>8

* Mon Sep 16 2019 Derek Ditch <derek@rocknsm.io> 0.54-1
- Bump version to 0.54 for Zeek 3.0

* Fri Aug 23 2019 Derek Ditch <derek@rocknsm.io> 0.53-1
- Bump version to 0.53

* Wed Feb 13 2019 Derek Ditch <derek@rocknsm.io> 0.51-1
- Initial RPM packaging
