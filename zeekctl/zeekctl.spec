%global __python %{python3}

Name:           zeekctl
Version:        2.1.0
Release:        1%{?dist}
Summary:        Tool for managing Zeek deployments.

License:        BSD
URL:            https://github.com/zeek/zeekctl
Source0:        https://download.zeek.org/%{name}-%{version}.tar.gz
Source1:        zeek.service

Provides:       broctl
Obsoletes:      broctl < 2.0.0

%if 0%{?rhel} < 8
BuildRequires:    cmake3  >= 3.0.0
%global cmake %cmake3
%else
BuildRequires:    cmake   >= 3.0.0
%endif 

BuildRequires:  python3-devel
BuildRequires:  python3-libs
BuildRequires:  python3-pysubnettree

BuildRequires:  capstats
BuildRequires:  trace-summary >= 0.90
BuildRequires:  systemd
BuildRequires:  zeek-core >= 3.1.0
BuildRequires:  /usr/sbin/sendmail


Requires:       zeek-core >= 3.1.0
Requires:       python3
Requires:       python3-libs
Requires:       python3-pysubnettree
Requires:       python3-broker

Requires:       bash
Requires:       capstats
Requires:       trace-summary >= 0.90
Requires:       /usr/sbin/sendmail


Requires(pre):    /usr/bin/getent
Requires(pre):    /usr/sbin/groupadd
Requires(pre):    /usr/sbin/useradd
Requires(post):   systemd
Requires(preun):  systemd
Requires(postun): systemd

%description
ZeekControl is an interactive interface for managing a Zeek installation which
allows you to, e.g., start/stop the monitoring or update its configuration.

%prep
%autosetup

# Remove aux packages to prefer rpm versions
rm -rf aux/*

# Fix the hard-coded paths in ZeekControl options
sed -E -i.orig '
  /("LibDir"|"PluginZeekDir")/s|/lib|%{_libdir}|;
  /LibDirInternal/s|/lib/zeekctl|%{python3_sitelib}/ZeekControl|;
  s|(%{_exec_prefix})+||
' ZeekControl/options.py

# Shebang
sed -i -e '1i#! /usr/bin/bash' bin/set-zeek-path bin/helpers/to-bytes.awk

%build
mkdir build; cd build
%cmake \
  -DZEEK_ROOT_DIR=%{_prefix} \
  -DZEEK_ETC_INSTALL_DIR=%{_sysconfdir}/zeek \
  -DZEEK_SCRIPT_INSTALL_PATH=%{_datadir}/zeek \
  -DPY_MOD_INSTALL_DIR=%{python3_sitelib} \
  -DZEEK_LOCAL_STATE_DIR:PATH=%{_localstatedir} \
  -DZEEK_SPOOL_DIR:PATH=%{_localstatedir}/spool/zeek \
  -DZEEK_LOG_DIR:PATH=%{_localstatedir}/log/zeek \
..
%make_build

%install
rm -rf $RPM_BUILD_ROOT
cd build
%make_install

# Install service file
%{__install} -D -c -m 644 %{SOURCE1} %{buildroot}%{_unitdir}/zeek.service

# Install config
%{__install} -d -m 755 %{buildroot}%{_sysconfdir}/zeek

# Create log dirs
%{__install} -d -m 755 %{buildroot}%{_localstatedir}/log/zeek
%{__install} -d -m 755 %{buildroot}%{_localstatedir}/log/zeek/archive
%{__install} -d -m 755 %{buildroot}%{_localstatedir}/log/zeek/sorted-logs
%{__install} -d -m 755 %{buildroot}%{_localstatedir}/log/zeek/stats

# Create spool dir
%{__install} -d -m 755 %{buildroot}%{_localstatedir}/spool/zeek
%{__install} -d -m 755 %{buildroot}%{_localstatedir}/spool/zeek/tmp

# Fix zeekctl python location
mkdir -p %{buildroot}%{python3_sitelib}
mv %{buildroot}/usr/lib/zeekctl/ZeekControl/ %{buildroot}%{python3_sitelib}/ZeekControl/
mv %{buildroot}/usr/lib/zeekctl/BroControl/ %{buildroot}%{python3_sitelib}/BroControl/
mv %{buildroot}/usr/lib/zeekctl/plugins %{buildroot}%{python3_sitelib}/ZeekControl/plugins

# Python byte compile zeekctl module
#%py_byte_compile %{python3} %{buildroot}%{py_sitedir}

################################################################################
%pre
getent group zeek >/dev/null || groupadd -r zeek
getent passwd zeek >/dev/null || \
    useradd -r -g zeek -d %{_localstatedir}/lib/zeek/ -s /sbin/nologin \
    -c "System account for Zeek service" zeek

exit 0

################################################################################
%post
%systemd_post zeek.service

exit 0

################################################################################
%preun
%systemd_preun zeek.service

################################################################################
%postun
%systemd_postun zeek.service

%files
%doc

%dir %{_sysconfdir}/zeek
%config(noreplace) %{_sysconfdir}/zeek/zeekctl.cfg
%config(noreplace) %{_sysconfdir}/zeek/node.cfg
%config(noreplace) %{_sysconfdir}/zeek/networks.cfg
%{_unitdir}/zeek.service
%dir %{_datadir}/zeekctl
%{_datadir}/zeek/zeekctl/*.zeek
%{_prefix}/lib/broctl
%{_bindir}/broctl
%{_bindir}/zeekctl
%{python3_sitelib}/BroControl
%{python3_sitelib}/ZeekControl
%{_mandir}/man8/zeekctl.8*

%dir %attr(-, zeek, zeek) %{_localstatedir}/log/zeek/
%dir %attr(-, zeek, zeek) %{_localstatedir}/spool/zeek/
%ghost %{_localstatedir}/log/zeek/*
%ghost %{_localstatedir}/spool/zeek/*

%dir %{_datadir}/zeek/zeekctl

# Needed if user moves the /var/spool/zeek directory elsewhere
%attr(-, zeek, zeek) %{_datadir}/zeekctl/scripts/

%changelog
* Thu May 21 2020 Derek Ditch <derek@rocknsm.io> 2.1.0-1
- Updated for Zeek 3.1.x

* Tue Sep 24 2019 Derek Ditch <derek@rocknsm.io> 2.0.0-2
- Updated for Zeek 3.0.0

* Thu Aug 22 2019 Bradford Dabbs <brad@dabbs.io> 2.0.0-1
- Bumped version to upstream 2.0