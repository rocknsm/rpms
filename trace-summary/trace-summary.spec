Name:           trace-summary
Version:        0.89
Release:        1%{?dist}
Summary:        Generates network traffic summaries.

License:        BSD
URL:            https://github.com/zeek/trace-summary
Source0:        https://www.zeek.org/downloads/%{name}-%{version}.tar.gz

Requires:       pysubnettree
Requires:       python

%description
trace-summary is a Python script that generates break-downs of
network traffic, including lists of the top hosts, protocols,
ports, etc. Optionally, it can generate output separately for
incoming vs. outgoing traffic, per subnet, and per time-interval.

%prep
%setup -q

%install
rm -rf $RPM_BUILD_ROOT
%{__install} -D trace-summary %{buildroot}%{_bindir}/trace-summary

%files
%doc README
%doc CHANGES
%license COPYING
%{_bindir}/trace-summary

%changelog
* Thu Aug 22 2019 Bradford Dabbs <brad@dabbs.io> 0.89-1
- Version bump

* Wed Feb 13 2019 Derek Ditch <derek@rocknsm.io> 0.88-1
- Initial RPM package
