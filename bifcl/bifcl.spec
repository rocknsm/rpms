%if 0%{?rhel} < 8
%global scl devtoolset-8
%global scl_prefix devtoolset-8-
%global scl_enable cat << EOSCL | scl enable %{scl} -
%global scl_disable EOSCL
%endif

Name:           bifcl
Version:        1.2
Release:        1%{?dist}
Epoch:          1
Summary:        Built-In-Function (BIF) Compiler/Generator for Zeek

License:        BSD
URL:            https://github.com/zeek/bifcl
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
The bifcl program simply takes a .bif file as input and
generates C++ header/source files along with a .bro script
that all-together provide the declaration and implementation of Bro
Built-In-Functions (BIFs), which can then be compiled and shipped
as part of a Bro plugin.

%prep
%autosetup

%build
mkdir build; cd build
%{?scl_enable} 
%cmake ..
%make_build
%{?scl_disable}

%install
rm -rf %{buildroot}
%{?scl_enable} 
%make_install --directory=build
%{?scl_disable}

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%doc README
%doc CHANGES
%license COPYING
%{_bindir}/bifcl

%changelog
* Wed May 20 2020 Derek Ditch <derek@rocknsm.io> 1.2-2
- Build with cmake3 and gcc > 8

* Mon Sep 16 2019 Derek Ditch <derek@rocknsm.io> 1.2-1
- Bump version to 1.2 for Zeek 3.0

* Wed Feb 13 2019 Derek Ditch <derek@rocknsm.io> 1.1-1
- Initial RPM packaging
