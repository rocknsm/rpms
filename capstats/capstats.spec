
%if 0%{?rhel} < 8
%global scl devtoolset-8
%global scl_prefix devtoolset-8-
%global scl_enable cat << EOSCL | scl enable %{scl} -
%global scl_disable EOSCL
%endif


Name:           capstats
Version:        0.28
Release:        1%{?dist}
Summary:        A tool to get some NIC statistics.

License:        BSD
URL:            https://github.com/zeek/capstats
Source0:        https://download.zeek.org/%{name}-%{version}.tar.gz

%if 0%{?rhel} < 8
BuildRequires:    cmake3
%global cmake %cmake3
%else
BuildRequires:    cmake
%endif
BuildRequires:  %{?scl_prefix}gcc-c++ >= 8
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
%{?scl_enable}
%cmake ..
%{?scl_disable}
%{?scl_enable}
%make_build
%{?scl_disable}

%install
rm -rf $RPM_BUILD_ROOT
%{?scl_enable}
%make_install
%{?scl_disable}

%files
%doc README
%doc CHANGES
%license COPYING
%caps(cap_net_admin,cap_net_raw=pie) %{_bindir}/capstats

%changelog
* Thu May 21 2020 Derek Ditch <derek@rocknsm.io> 0.28-1
- Bump to 0.28
- Compile with g++ > 8 and cmake3

* Wed Aug 21 2019 Derek Ditch <derek@rocknsm.io> 0.27-1
- Bump to 0.27

* Wed Feb 13 2019 Derek Ditch <derek@rocknsm.io> 0.26-1
- Initial RPM package
