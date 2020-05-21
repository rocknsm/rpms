%global     distname zeek-af_packet-plugin

%if 0%{?rhel} < 8
%global scl devtoolset-8
%global scl_prefix devtoolset-8-
%global scl_enable cat << EOSCL | scl enable %{scl} -
%global scl_disable EOSCL
%endif

Name:       zeek-plugin-af_packet
Version:    2.0.0
Release:    1%{?dist}
Epoch:      2
Summary:    Native AF_Packet support plugin for Zeek.

License:    BSD
URL:        https://github.com/J-Gras/%{distname}/
Source0:    https://github.com/J-Gras/%{distname}/archive/%{version}.tar.gz#/%{distname}-%{version}.tar.gz

%if 0%{?rhel} < 8
BuildRequires:    cmake3  >= 3.0.0
%global cmake %cmake3
%else
BuildRequires:    cmake   >= 3.0.0
%endif 
BuildRequires:  kernel-devel
BuildRequires:  libpcap-devel
BuildRequires:  zlib-devel
BuildRequires:  zeek-devel = 3.1.3
BuildRequires:  bifcl = 1:1.2
BuildRequires:  binpac-devel = 1:0.55.1
BuildRequires:  binpac = 1:0.55.1
BuildRequires:  %{?scl_prefix}gcc-c++ >= 8
Requires:       zeek-core = 3.1.3
Requires:       libpcap
Requires:       zlib

Obsoletes:      bro-plugin-af_packet < 2:1.4.0-4
Provides:       bro-plugin-af_packet = %{version}-%{release}

%description
This plugin provides native AF_Packet support for Bro.

%prep
%autosetup -n %{distname}-%{version}

%build
mkdir build; cd build
%{?scl_enable}
%cmake \
  -DCMAKE_MODULE_PATH=%{_datadir}/zeek/cmake \
  -DBRO_CONFIG_CMAKE_DIR=%{_datadir}/zeek/cmake \
  -DBRO_CONFIG_PLUGIN_DIR=%{_libdir}/zeek/plugins \
  -DBRO_CONFIG_PREFIX=%{_prefix} \
  -DBRO_CONFIG_INCLUDE_DIR=%{_includedir}/zeek \
  -DKERNELHEADERS_LATEST:BOOL=ON \
  ..
%{?scl_disable}

%{?scl_enable}
%make_build
%{?scl_disable}

%install
cd build
%{?scl_enable}
%make_install
%{?scl_disable}

%files
%doc README MAINTAINER VERSION
%license COPYING

%{_libdir}/zeek/plugins/Zeek_AF_Packet/

%changelog
* Wed May 20 2020 Derek Ditch <derek@rocknsm.io> 2.0.0-1
- Version bump upstream, renamed Bro to Zeek
- Compiled with gcc > 8 and cmake3
- Simplify files list

* Mon Dec 16 2019 Derek Ditch <derek@rocknsm.io> 1.4.0-5
- Recompile against Zeek 3.0.1

* Tue Sep 24 2019 Derek Ditch <derek@rocknsm.io> 1.4.0-4
- Recompile against Zeek 3.0.0

* Thu Sep 5 2019 Derek Ditch <derek@rocknsm.io> 1.4.0-3
- Recompile against Bro 2.6.4

* Fri Aug 23 2019 Bradford Dabbs <brad@dabbs.io> 1.4.0-2
- Change requirements to build against Bro 2.6.3

* Thu Feb 14 2019 Derek Ditch <derek@rocknsm.io> 1.4.0-1
- Version bump to 1.4.0
- Move to cmake build process against 2.6.1
* Wed Oct 24 2018 Derek Ditch <derek@rocknsm.io> 1.3-2
- Rebuilding to lock against bro 2.5.5
- Added gcc-c++ as build dependency

* Mon Aug 13 2018 Derek Ditch <derek@rocknsm.io> 1.3-1
- Rebuilding to lock against bro 2.5.4
