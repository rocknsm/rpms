%global     distname metron-bro-plugin-kafka
%global     commit0 bfc9cbbdc97c3a12c59e9d9786bd7e3996a196f5
%global     shortcommit0 %(c=%{commit0}; echo ${c:0:7})
%global     commitdate 20190214

Name:       bro-plugin-kafka
Version:    0.3
Release:    3.%{commitdate}git%{shortcommit0}%{?dist}
Epoch:      1
Summary:    A Bro log writer plugin that sends logging output to Kafka.

License:    ASL 2.0
URL:        https://github.com/apache/%{distname}
Source0:    https://github.com/apache/%{distname}/archive/%{commit0}.tar.gz#/%{name}-%{shortcommit0}.tar.gz

BuildRequires:  cmake
BuildRequires:  librdkafka-devel
BuildRequires:  openssl-devel
BuildRequires:  libpcap-devel
BuildRequires:  bro-devel = 2.6.1
BuildRequires:  bifcl = 1:1.1
BuildRequires:  binpac-devel = 1:0.51
BuildRequires:  binpac = 1:0.51
BuildRequires:  gcc-c++
Requires:       bro-core  = 2.6.1
Requires:       librdkafka = 0.11.5
Requires:       openssl

%description
A Bro log writer plugin that sends logging output to Kafka.

%prep
%setup -n %{distname}-%{commit0}

%build
# ./configure --build=x86_64-redhat-linux-gnu --host=x86_64-redhat-linux-gnu --program-prefix= --disable-dependency-tracking --prefix=/usr --exec-prefix=/usr --bindir=/usr/bin --sbindir=/usr/sbin --sysconfdir=/etc --datadir=/usr/share --includedir=/usr/include --libdir=/usr/lib64 --libexecdir=/usr/libexec --localstatedir=/var --sharedstatedir=/var/lib --mandir=/usr/share/man --infodir=/usr/share/info --bro-dist=/usr/src/bro-2.5.1
mkdir build; cd build
%cmake \
  -DCMAKE_MODULE_PATH=/usr/share/bro/cmake \
  -DBRO_CONFIG_CMAKE_DIR=/usr/share/bro/cmake \
  -DBRO_CONFIG_PLUGIN_DIR=/usr/lib64/bro/plugins \
  -DBRO_CONFIG_PREFIX=/usr \
  -DBRO_CONFIG_INCLUDE_DIR=/usr/include/bro \
  ..
%make_build

%install
%make_install

%files
%dir %{_libdir}/bro/plugins/APACHE_KAFKA/
%dir %{_libdir}/bro/plugins/APACHE_KAFKA/lib
%dir %{_libdir}/bro/plugins/APACHE_KAFKA/lib/bif
%dir %{_libdir}/bro/plugins/APACHE_KAFKA/scripts
%dir %{_libdir}/bro/plugins/APACHE_KAFKA/scripts/Apache
%dir %{_libdir}/bro/plugins/APACHE_KAFKA/scripts/Apache/Kafka

%{_libdir}/bro/plugins/APACHE_KAFKA/CHANGES
%{_libdir}/bro/plugins/APACHE_KAFKA/COPYING
%{_libdir}/bro/plugins/APACHE_KAFKA/VERSION
%{_libdir}/bro/plugins/APACHE_KAFKA/__bro_plugin__
%{_libdir}/bro/plugins/APACHE_KAFKA/lib/APACHE-KAFKA.linux-x86_64.so
%{_libdir}/bro/plugins/APACHE_KAFKA/lib/bif/*.bro
%{_libdir}/bro/plugins/APACHE_KAFKA/scripts/Apache/Kafka/*.bro
%{_libdir}/bro/plugins/APACHE_KAFKA/scripts/*.bro

%doc README.md COPYING MAINTAINER VERSION CHANGES

%changelog
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
