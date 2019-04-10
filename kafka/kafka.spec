%define __jar_repack 0
%define debug_package %{nil}
%define scala_version 2.12
%define _prefix      %{_datadir}/kafka
%define _conf_dir    %{_sysconfdir}/kafka
%define _log_dir     %{_var}/log/kafka
%define _data_dir    %{_sharedstatedir}/kafka

Name:    kafka
Version: 2.2.0
Release: 1%{dist}
Summary: Apache Kafka is publish-subscribe messaging rethought as a distributed commit log.

License: Apache License, Version 2.0
URL:     http://kafka.apache.org/
Source0: https://www-us.apache.org/dist/%{name}/%{version}/%{name}_%{scala_version}-%{version}.tgz

Provides: kafka = %{version}
Provides: kafka-server = %{version}

Prefix:  %{_prefix}

BuildRequires: systemd
Requires(post): systemd
Requires(preun): systemd
Requires(postun): systemd
Requires: java-11-openjdk-headless

%description
Kafka is designed to allow a single cluster to serve as the central data backbone for a large organization. It can be elastically and transparently expanded without downtime. Data streams are partitioned and spread over a cluster of machines to allow data streams larger than the capability of any single machine and to allow clusters of co-ordinated consumers. Messages are persisted on disk and replicated within the cluster to prevent data loss.

%prep
%autosetup -n %{name}_%{scala_version}-%{version}

%build
rm -f libs/{*-javadoc.jar,*-scaladoc.jar,*-sources.jar,*-test.jar}

%install
mkdir -p %{buildroot}%{_prefix}/{libs,bin,config}
mkdir -p %{buildroot}%{_log_dir}
mkdir -p %{buildroot}%{_data_dir}
mkdir -p %{buildroot}%{_unitdir}
mkdir -p %{buildroot}%{_conf_dir}/
install -p -D -m 755 bin/*.sh %{buildroot}%{_prefix}/bin
install -p -D -m 644 config/* %{buildroot}%{_prefix}/config
install -p -D -m 644 config/server.properties %{buildroot}%{_conf_dir}/
sed -i "s:^log.dirs=.*:log.dirs=%{_data_dir}:" %{buildroot}%{_conf_dir}/server.properties
install -p -D -m 755 kafka.service %{buildroot}%{_unitdir}/kafka.service
install -p -D -m 644 kafka.logrotate %{buildroot}%{_sysconfdir}/logrotate.d/kafka
install -p -D -m 644 log4j.properties %{buildroot}%{_conf_dir}/log4j.properties
install -p -D -m 644 kafka.sysconfig %{buildroot}%{_sysconfdir}/sysconfig/kafka
install -p -D -m 644 libs/* %{buildroot}%{_sharedstatedir}/kafka

%clean
rm -rf %{buildroot}

%pre
/usr/bin/getent group kafka >/dev/null || /usr/sbin/groupadd -r kafka
if ! /usr/bin/getent passwd kafka >/dev/null ; then
    /usr/sbin/useradd -r -g kafka -d %{_prefix} -s /bin/nologin -c "Kafka system account" kafka
fi

%post
%systemd_post kafka.service

%preun
%systemd_preun kafka.service

%postun
%systemd_postun

%files
%doc NOTICE
%license LICENSE

%defattr(-,root,root)
%{_unitdir}/kafka.service
%config(noreplace) %{_sysconfdir}/logrotate.d/kafka
%config(noreplace) %{_sysconfdir}/sysconfig/kafka
%config(noreplace) %{_conf_dir}/*
%{_prefix}
%attr(0755,kafka,kafka) %dir %{_log_dir}
%attr(0700,kafka,kafka) %dir %{_data_dir}
