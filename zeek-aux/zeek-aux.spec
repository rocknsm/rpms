%if 0%{?rhel} < 8
%global scl devtoolset-8
%global scl_prefix devtoolset-8-
%global scl_enable cat << EOSCL | scl enable %{scl} -
%global scl_disable EOSCL
%endif

Name:           zeek-aux
Version:        0.50
Release:        1%{?dist}
Epoch:          1
Summary:        Zeek Auxiliary Programs

License:        BSD
URL:            https://github.com/zeek/zeek-aux
Source0:        https://download.zeek.org/%{name}-%{version}.tar.gz

Provides:       bro-aux
Obsoletes:      bro-aux < 0.43

BuildRequires:  bind-devel
BuildRequires:  libpcap-devel
BuildRequires:  openssl-devel
BuildRequires:  flex
%if 0%{?rhel} < 8
BuildRequires:    cmake3  >= 3.0.0
%global cmake %cmake3
%else
BuildRequires:    cmake   >= 3.0.0
%endif
BuildRequires:    %{?scl_prefix}gcc-c++ >= 8

Requires:       libpcap

%description


%prep
%autosetup


%build
mkdir build; cd build
%{?scl_enable}
%cmake ..
%{?scl_disable}

%{?scl_enable}
%make_build

%install
rm -rf $RPM_BUILD_ROOT
%{?scl_enable}
%make_install
%{?scl_disable}

%files
%doc README
%doc CHANGES
%license COPYING
%{_bindir}/adtrace
%{_bindir}/bro-cut
%{_bindir}/zeek-cut
%{_bindir}/rst
%{_mandir}/man1/zeek-cut.1.gz


%changelog
* Wed May 20 2020 Derek Ditch <derek@rocknsm.io> 0.44-1
- Version bump for upstream
- Build with g++ > 8 and cmake3

* Mon Aug 26 2019 Derek Ditch <derek@rocknsm.io> 0.43-3
- Obsoletes bro-aux

* Thu Aug 22 2019 Bradford Dabbs <brad@dabbs.io> 0.43-1
- Packaging zeek-aux vs bro-aux
