Name:           bifcl
Version:        1.1
Release:        1%{?dist}
Epoch:          1
Summary:        Built-In-Function (BIF) Compiler/Generator for Zeek

License:        BSD
URL:            https://github.com/zeek/bifcl
Source0:        https://www.zeek.org/downloads/%{name}-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  cmake >= 2.8.12
BuildRequires:  flex
BuildRequires:  bison
BuildRequires:  gcc-c++

%description
The bifcl program simply takes a .bif file as input and
generates C++ header/source files along with a .bro script
that all-together provide the declaration and implementation of Bro
Built-In-Functions (BIFs), which can then be compiled and shipped
as part of a Bro plugin.

%prep
%setup -q

%build
mkdir build; cd build
%cmake ..
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
%{_bindir}/bifcl

%changelog

* Wed Feb 13 2019 Derek Ditch <derek@rocknsm.io> 1.1-1
- Initial RPM packaging
