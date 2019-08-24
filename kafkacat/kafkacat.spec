Name:     kafkacat
Version:  1.4.0
Release:  1%{?dist}
Summary:  Generic command line non-JVM Apache Kafka producer and consumer
License:  BSD-2-Clause
URL:      https://github.com/edenhill/%{name}
Source:   https://github.com/edenhill/%{name}/archive/%{version}.tar.gz#/%{name}-%{version}.tar.gz
Requires: librdkafka yajl

BuildRequires: zlib-devel 
BuildRequires: gcc >= 4.1 
BuildRequires: librdkafka-devel 
BuildRequires: yajl-devel
Requires: zlib
Requires: yajl
Requires: librdkafka

%description
kafkacat is a generic non-JVM producer and consumer for Apache Kafka,
think of it as a netcat for Kafka.

In producer mode kafkacat reads messages from stdin, delimited with a
configurable delimeter (-D, defaults to newline), and produces them to the
provided Kafka cluster (-b), topic (-t) and partition (-p).

In consumer mode kafkacat reads messages from a topic and partition and prints
them to stdout using the configured message delimiter.

kafkacat also features a Metadata list (-L) mode to display the current state
of the Kafka cluster and its topics and partitions.

kafkacat is fast and lightweight; statically linked it is no more than 150Kb.

%prep
%setup -q

%configure

%build
%make_build

%install
%make_install

%files -n %{name}
%defattr(755,root,root)
%{_bindir}/kafkacat
%defattr(644,root,root)
%doc README.md
%doc LICENSE

%changelog
* Fri Aug 23 2019 Derek Ditch <derek@rocknsm.io> 1.4.0-1
- Version bump to 1.4.0

* Thu Oct 12 2017 Derek Ditch <derek@rocknsm> 1.3.1-1
- Update to upstream 1.3.1
- Add yajl to dependencies

* Wed Jun 03 2015 Magnus Edenhill <magnus@edenhill.se> 1.2.0-1
- Relase 1.2.0

* Fri Dec 19 2014 François Saint-Jacques <fsaintjacques@gmail.com> 1.1.0-1
- Initial RPM package
