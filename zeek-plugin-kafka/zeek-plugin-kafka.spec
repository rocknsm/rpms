%global     distname metron-bro-plugin-kafka
%global     commit0 43c9166787649e4ac2ab295a1baba94d54903651
%global     shortcommit0 %(c=%{commit0}; echo ${c:0:7})
%global     commitdate 20190429

Name:       zeek-plugin-kafka
Version:    0.3
Release:    5.%{commitdate}git%{shortcommit0}%{?dist}
Epoch:      1
Summary:    A Zeek log writer plugin that sends logging output to Kafka.

License:    ASL 2.0
URL:        https://github.com/apache/%{distname}
Source0:    https://github.com/apache/%{distname}/archive/%{commit0}.tar.gz#/%{name}-%{shortcommit0}.tar.gz

BuildRequires:  cmake
BuildRequires:  librdkafka-devel
BuildRequires:  openssl-devel
BuildRequires:  libpcap-devel
BuildRequires:  zeek-devel = 3.0.0
BuildRequires:  bifcl = 1:1.2
BuildRequires:  binpac-devel = 1:0.54
BuildRequires:  binpac = 1:0.54
BuildRequires:  gcc-c++
Requires:       zeek-core  = 3.0.0
Requires:       librdkafka = 0.11.5
Requires:       openssl

Obsoletes:      bro-plugin-kafka < 0.3-5
Provides:       bro-plugin-kafka = %{version}-%{release}

%description
A Bro log writer plugin that sends logging output to Kafka.

%prep
%autosetup -n %{distname}-%{commit0}

%build
mkdir build; cd build
%cmake \
  -DCMAKE_MODULE_PATH=%{_datadir}/zeek/cmake \
  -DBRO_CONFIG_CMAKE_DIR=%{_datadir}/zeek/cmake \
  -DBRO_CONFIG_PLUGIN_DIR=%{_libdir}/zeek/plugins \
  -DBRO_CONFIG_PREFIX=%{_prefix} \
  -DBRO_CONFIG_INCLUDE_DIR=%{_includedir}/zeek \
  ..
%make_build

%install
%make_install

%files
%dir %{_libdir}/zeek/plugins/APACHE_KAFKA/
%dir %{_libdir}/zeek/plugins/APACHE_KAFKA/lib
%dir %{_libdir}/zeek/plugins/APACHE_KAFKA/lib/bif
%dir %{_libdir}/zeek/plugins/APACHE_KAFKA/scripts
%dir %{_libdir}/zeek/plugins/APACHE_KAFKA/scripts/Apache
%dir %{_libdir}/zeek/plugins/APACHE_KAFKA/scripts/Apache/Kafka

%{_libdir}/zeek/plugins/APACHE_KAFKA/CHANGES
%{_libdir}/zeek/plugins/APACHE_KAFKA/COPYING
%{_libdir}/zeek/plugins/APACHE_KAFKA/VERSION
%{_libdir}/zeek/plugins/APACHE_KAFKA/__bro_plugin__
%{_libdir}/zeek/plugins/APACHE_KAFKA/lib/APACHE-KAFKA.linux-x86_64.so
%{_libdir}/zeek/plugins/APACHE_KAFKA/lib/bif/*.zeek
%{_libdir}/zeek/plugins/APACHE_KAFKA/scripts/Apache/Kafka/*.bro
%{_libdir}/zeek/plugins/APACHE_KAFKA/scripts/*.bro

%doc README.md COPYING MAINTAINER VERSION CHANGES

%changelog
* Tue Sep 24 2019 Derek Ditch <derek@rocknsm.io> 0.3-6
- Recompile against Zeek 3.0.0

* Thu Sep 5 2019 Derek Ditch <derek@rocknsm.io> 0.3-5
- Recompile against Bro 2.6.4

* Fri Aug 23 2019 Bradford Dabbs <brad@dabbs.io> 0.3-4
- Updated to latest commit upstream
- Updated Bro requirement to 2.6.3

* Thu Feb 14 2019 Derek Ditch <derek@rocknsm.io> 0.3-3
- Updated to latest commit upstream (technically pre-0.3)
- Fix segfault on plugin exit
- Allow sending log to multiple topics

* Fri Oct 26 2018 Derek Ditch <derek@rocknsm.io> 0.3-2
- Update librdkafka requirement to 0.11.5

* Wed Oct 24 2018 Derek Ditch <derek@rocknsm.io> 0.3-1
- Updating to upstream version
- Update to link against Bro 2.5.5

* Mon Aug 13 2018 Derek Ditch <derek@rocknsm.io> 0.2-3
- Rebuilding to lock against librdkafka 0.11.4

* Thu Apr 05 2018 Derek Ditch <derek@rocknsm.io> 0.2-2
- Rebuilding to link against librdkafka 0.11.4

* Thu Apr 05 2018 Derek Ditch <derek@rocknsm.io> 0.2-1
- Updated to latest upstream
- Integrates configurable JSON timestamps
- Removes "send all logs by default" option
