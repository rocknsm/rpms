%global     distname metron-bro-plugin-kafka
%global     commit0 1dfc5239fae31a64026188109d1e346ce93d5c02
%global     shortcommit0 %(c=%{commit0}; echo ${c:0:7})
%global     commitdate 20180317

Name:       bro-plugin-kafka
Version:    0.2
Release:    2.%{commitdate}git%{shortcommit0}%{?dist}
Epoch:      1
Summary:    A Bro log writer plugin that sends logging output to Kafka.

License:    ASL 2.0
URL:        https://github.com/apache/%{distname}
Source0:    https://github.com/apache/%{distname}/archive/%{commit0}.tar.gz#/%{name}-%{shortcommit0}.tar.gz

BuildRequires:  cmake
BuildRequires:  librdkafka-devel
BuildRequires:  openssl-devel
BuildRequires:  libpcap-devel
BuildRequires:  bro-devel >= 2.5.0
Requires:       bro-core  >= 2.5.0
Requires:       librdkafka >= 0.9.4
Requires:       openssl

%description
A Bro log writer plugin that sends logging output to Kafka.

%prep
%setup -n %{distname}-%{commit0}

%build
# ./configure --build=x86_64-redhat-linux-gnu --host=x86_64-redhat-linux-gnu --program-prefix= --disable-dependency-tracking --prefix=/usr --exec-prefix=/usr --bindir=/usr/bin --sbindir=/usr/sbin --sysconfdir=/etc --datadir=/usr/share --includedir=/usr/include --libdir=/usr/lib64 --libexecdir=/usr/libexec --localstatedir=/var --sharedstatedir=/var/lib --mandir=/usr/share/man --infodir=/usr/share/info --bro-dist=/usr/src/bro-2.5.1
BRO_DIST=$(find /usr/src -name bro-config -exec /bin/sh {} --bro_dist \;)
./configure --bro-dist=${BRO_DIST}
make %{?_smp_mflags}


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
* Thu Apr 05 2018 Derek Ditch <derek@rocknsm.io> 0.2-2
- Rebuilding to link against librdkafka 0.11.4

* Thu Apr 05 2018 Derek Ditch <derek@rocknsm.io> 0.2-1
- Updated to latest upstream
- Integrates configurable JSON timestamps
- Removes "send all logs by default" option

