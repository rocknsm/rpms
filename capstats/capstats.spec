Name:           capstats
Version:        0.26
Release:        1%{?dist}
Summary:        A tool to get some NIC statistics.

License:        BSD
URL:            https://github.com/zeek/capstats
Source0:        https://www.zeek.org/downloads/%{name}-%{version}.tar.gz

BuildRequires:  cmake >= 2.6.3
BuildRequires:  gcc-c++
BuildRequires:  libpcap-devel
Requires:       libpcap

%description
capstats is a small tool to collect statistics on the current load of a network
interface, using libpcap. It reports statistics per time interval and/or for
the tool's total run-time.

%prep
%setup -q

%build
mkdir build; cd build
%cmake ..
%make_build


%install
rm -rf $RPM_BUILD_ROOT
%make_install

%files
%doc README
%doc CHANGES
%license COPYING
%caps(cap_net_admin,cap_net_raw=pie) %{_bindir}/capstats

%changelog
* Wed Feb 13 2019 Derek Ditch <derek@rocknsm.io> 0.26-1
- Initial RPM package
