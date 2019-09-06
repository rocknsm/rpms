%global     distname bro-af_packet-plugin
# %global     commit0 79edee2bf830becfe47cec11c1ce5eb24fc285dc
# %global     shortcommit0 %(c=%{commit0}; echo ${c:0:7})
# %global     commitdate 20171122

Name:       bro-plugin-af_packet
Version:    1.4.0
Release:    2%{?dist}
Epoch:      2
Summary:    Native AF_Packet support plugin for Bro.

License:    BSD
URL:        https://github.com/J-Gras/bro-af_packet-plugin/
#Source0:    https://github.com/J-Gras/%{distname}/archive/%{commit0}.tar.gz#/%{name}-%{shortcommit0}.tar.gz
Source0:    https://github.com/J-Gras/%{distname}/archive/%{version}.tar.gz

BuildRequires:  cmake
BuildRequires:  kernel-devel
BuildRequires:  libpcap-devel
BuildRequires:  zlib-devel
BuildRequires:  bro-devel = 2.6.4
BuildRequires:  bifcl = 1:1.1
BuildRequires:  binpac-devel = 1:0.53
BuildRequires:  binpac = 1:0.53
BuildRequires:  gcc-c++
Requires:       bro-core = 2.6.4
Requires:       libpcap
Requires:       zlib

%description
This plugin provides native AF_Packet support for Bro.

%prep
%setup -n %{distname}-%{version}

# ./configure --build=x86_64-redhat-linux-gnu --host=x86_64-redhat-linux-gnu --program-prefix= --disable-dependency-tracking --prefix=/usr --exec-prefix=/usr --bindir=/usr/bin --sbindir=/usr/sbin --sysconfdir=/etc --datadir=/usr/share --includedir=/usr/include --libdir=/usr/lib64 --libexecdir=/usr/libexec --localstatedir=/var --sharedstatedir=/var/lib --mandir=/usr/share/man --infodir=/usr/share/info --bro-dist=/usr/src/bro-2.5.1


%build
mkdir build; cd build
%cmake \
  -DCMAKE_MODULE_PATH=%{_datadir}/bro/cmake \
  -DBRO_CONFIG_CMAKE_DIR=%{_datadir}/bro/cmake \
  -DBRO_CONFIG_PLUGIN_DIR=%{_libdir}/bro/plugins \
  -DBRO_CONFIG_PREFIX=%{_prefix} \
  -DBRO_CONFIG_INCLUDE_DIR=%{_includedir}/bro \
  -DKERNELHEADERS_LATEST:BOOL=ON \
  ..
make %{?_smp_mflags}


%install
%make_install

%files
%dir %{_libdir}/bro/plugins/Bro_AF_Packet
%dir %{_libdir}/bro/plugins/Bro_AF_Packet/broctl
%dir %{_libdir}/bro/plugins/Bro_AF_Packet/lib
%dir %{_libdir}/bro/plugins/Bro_AF_Packet/lib/bif
%dir %{_libdir}/bro/plugins/Bro_AF_Packet/scripts

%{_libdir}/bro/plugins/Bro_AF_Packet/__bro_plugin__
%{_libdir}/bro/plugins/Bro_AF_Packet/broctl/af_packet.p*
%{_libdir}/bro/plugins/Bro_AF_Packet/lib/Bro-AF_Packet.linux-x86_64.so
%{_libdir}/bro/plugins/Bro_AF_Packet/lib/bif/*.bro
%{_libdir}/bro/plugins/Bro_AF_Packet/scripts/*.bro

%{_libdir}/bro/plugins/Bro_AF_Packet/README
%{_libdir}/bro/plugins/Bro_AF_Packet/VERSION
%{_libdir}/bro/plugins/Bro_AF_Packet/COPYING

%doc README MAINTAINER VERSION
%license COPYING


%changelog
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
