%define __jar_repack 0
#define debug_package %{nil}
%define zk_prefix     %{_javadir}/zookeeper
%define zk_confdir    %{_sysconfdir}/zookeeper
%define zk_logdir     %{_var}/log/zookeeper
%define zk_datadir    %{_sharedstatedir}/zookeeper

Summary: High-performance coordination service for distributed applications
Name: zookeeper
#Version: %{version}
#Release: %{release}%{?dist}
Version: 3.4.14
Release: 1%{?dist}
License: ASL 2.0 and BSD
Group: Applications/Databases
URL: https://zookeeper.apache.org/
Source0: https://www-us.apache.org/dist/%{name}/%{name}-%{version}/%{name}-%{version}.tar.gz
Source1: zookeeper.service
Source2: zkcli
Source3: zookeeper.logrotate
Source4: zookeeper.sysconfig
Source5: zoo.cfg
Source6: log4j.properties
Source7: log4j-cli.properties
%{?systemd_requires}
Requires: java-11-openjdk-headless
BuildRequires: systemd
BuildArch: noarch

%description
ZooKeeper is a high-performance coordination service for distributed
applications. It exposes common services - such as naming, configuration
management, synchronization, and group services - in a simple interface so
you don't have to write them from scratch. You can use it off-the-shelf to
implement consensus, group management, leader election, and presence
protocols. And you can build on it for your own, specific needs.

%prep
%setup -q

%build

%install
# JARs
mkdir -p %{buildroot}%{zk_prefix}
install -p -m 0644 zookeeper-%{version}.jar lib/*.jar \
  %{buildroot}%{zk_prefix}/
# Service, systemd fails to expand file paths in runtime
mkdir -p %{buildroot}%{_unitdir}
install -p -D -m 0644 %{S:1} %{buildroot}%{_unitdir}/zookeeper.service
CLASSPATH=
for i in %{buildroot}%{zk_prefix}/*.jar; do
  CLASSPATH="%{zk_prefix}/$(basename ${i}):${CLASSPATH}"
done
sed -e "s|@CLASSPATH@|${CLASSPATH}|" %{S:1} > \
  %{buildroot}%{_unitdir}/zookeeper.service
# CLI
install -p -D -m 0755 %{S:2} %{buildroot}%{_bindir}/zkcli
# Configuration
install -p -D -m 0644 %{S:3} %{buildroot}%{_sysconfdir}/logrotate.d/zookeeper
install -p -D -m 0644 %{S:4} %{buildroot}%{_sysconfdir}/sysconfig/zookeeper
mkdir -p %{buildroot}%{zk_confdir}/
install -p -m 0644 %{S:5} %{S:6} %{S:7} conf/configuration.xsl \
  %{buildroot}%{zk_confdir}/
# Empty directories
mkdir -p %{buildroot}%{zk_logdir}
mkdir -p %{buildroot}%{zk_datadir}

%pre
/usr/bin/getent group zookeeper >/dev/null || /usr/sbin/groupadd -r zookeeper
if ! /usr/bin/getent passwd zookeeper >/dev/null; then
  /usr/sbin/useradd -r -g zookeeper -M -N -d %{zk_prefix} -s /bin/bash -c "Zookeeper" zookeeper
fi

%post
%systemd_post zookeeper.service

%preun
%systemd_preun zookeeper.service

%postun
%systemd_postun_with_restart zookeeper.service

%files
%license LICENSE.txt
%{zk_prefix}/
%{_unitdir}/zookeeper.service
%{_bindir}/zkcli
%config(noreplace) %{_sysconfdir}/logrotate.d/zookeeper
%config(noreplace) %{_sysconfdir}/sysconfig/zookeeper
%dir %{zk_confdir}/
%config(noreplace) %{zk_confdir}/*
%attr(0755,zookeeper,zookeeper) %dir %{zk_logdir}/
%attr(0700,zookeeper,zookeeper) %dir %{zk_datadir}/

%changelog
* Wed Apr 10 2019 Bradford Dabbs <brad@perched.io> 3.4.14-1
- Bump version to 3.4.14
- Update source0 to https

* Tue Apr 9 2019 Bradford Dabbs <brad@perched.io> 3.4.13-2
- Explicitly specify Java 11

* Tue Mar 26 2019 Derek Ditch <derek@perched.io> 3.4.13-1
- Bump version
- Now requires java-headless

* Wed Jan 10 2018 Bradford Dabbs <bndabbs@gmail.com> 3.4.11-1
- Change zookeeper version from 3.4.9 to 3.4.11
- Add install command for zookeeper.service
