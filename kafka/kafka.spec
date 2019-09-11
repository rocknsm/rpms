%global __jar_repack 0
%global debug_package %{nil}
%global scala_version 2.12
%global _kafkadir    /usr/share/kafka
%global _conf_dir    %{_sysconfdir}/kafka
%global _log_dir     %{_localstatedir}/log/kafka

Name:    kafka
Version: 2.3.0
Release: 1%{dist}
Summary: Apache Kafka is publish-subscribe messaging rethought as a distributed commit log.

License: Apache License, Version 2.0
URL:     http://kafka.apache.org/
Source0: https://www-us.apache.org/dist/%{name}/%{version}/%{name}_%{scala_version}-%{version}.tgz
Source1: https://raw.githubusercontent.com/rocknsm/rpms/master/kafka/kafka.service
Source2: https://raw.githubusercontent.com/rocknsm/rpms/master/kafka/kafka.logrotate
Source3: https://raw.githubusercontent.com/rocknsm/rpms/master/kafka/kafka.sysconfig
Source4: https://raw.githubusercontent.com/rocknsm/rpms/master/kafka/log4j.properties

Provides: kafka = %{version}
Provides: kafka-server = %{version}

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

# Add system classpath as default for run-class script
sed -i '/^base_dir=.*/a \\n## Load system classpath for RPM install\nCLASSPATH=$(build-classpath kafka)' bin/kafka-run-class.sh

# Change default log paths
sed -i 's:^log.dirs=.*:log.dirs=%{_log_dir}:' config/server.properties

# Remove bundled zookeeper
rm -f libs/zookeeper*.jar
rm -f config/zookeeper.properties
rm -f bin/zookeeper*.sh

# Remove windows scripts
rm -rf bin/windows

%install
mkdir -p %{buildroot}%{_kafkadir}/{bin,config}
mkdir -p %{buildroot}%{_log_dir}
mkdir -p %{buildroot}%{_unitdir}
mkdir -p %{buildroot}%{_conf_dir}
mkdir -p %{buildroot}%{_javadir}/kafka
install -p -D -m 755 bin/*.sh %{buildroot}%{_kafkadir}/bin
install -p -D -m 644 config/* %{buildroot}%{_kafkadir}/config
install -p -D -m 644 config/server.properties %{buildroot}%{_conf_dir}/
install -p -D -m 644 libs/* %{buildroot}%{_javadir}/kafka
install -p -D -m 755 %{S:1} %{buildroot}%{_unitdir}/kafka.service
install -p -D -m 644 %{S:2} %{buildroot}%{_sysconfdir}/logrotate.d/kafka
install -p -D -m 644 %{S:3} %{buildroot}%{_sysconfdir}/sysconfig/kafka
install -p -D -m 644 %{S:4} %{buildroot}%{_conf_dir}/log4j.properties

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
%{_javadir}/kafka
%{_kafkadir}/bin
%{_kafkadir}/config
%attr(0755,kafka,kafka) %dir %{_log_dir}
%attr(0700,kafka,kafka) %dir %{_kafkadir}

%changelog
* Wed Sep 11 2019 Derek Ditch <derek@rocknsm.io> 2.3.0-1
- Version bump to 2.3.0
- Fix CLASSPATH in kafka scripts

* Wed Apr 10 2019 Bradford Dabbs <brad@perched.io> 2.2.0-1
- Initial build for ROCK NSM
