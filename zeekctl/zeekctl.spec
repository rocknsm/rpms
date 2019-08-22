Name:           zeekctl
Version:        2.0.0
Release:        1%{?dist}
Epoch:          1
Summary:        Tool for managing Zeek deployments.

License:        BSD
URL:            https://github.com/zeek/zeekctl
Source0:        https://www.zeek.org/downloads/%{name}-%{version}.tar.gz
Source1:        zeek.service

BuildRequires:  cmake >= 2.6.3
BuildRequires:  gcc-c++
BuildRequires:  python2-devel
BuildRequires:  capstats >= 0.26
BuildRequires:  trace-summary >= 0.88
BuildRequires:  systemd
BuildRequires:  swig
BuildRequires:  libpcap-devel
BuildRequires:  bro-core >= 2.6.1

Requires:       bro-core >= 2.6.3
Requires:       libpcap
Requires:       python2
Requires:       bash
Requires:       capstats
Requires:       trace-summary

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
%setup -q

# Fix the hard-coded paths in ZeekControl options
sed -E -i.orig '
  /("LibDir"|"PluginZeekDir")/s|/lib|%{_libdir}|;
  /LibDirInternal/s|/lib/zeekctl|%{python2_sitelib}/ZeekControl|;
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
  -DPY_MOD_INSTALL_DIR=%{python2_sitelib} \
  -DZEEK_LOCAL_STATE_DIR:PATH=%{_localstatedir} \
  -DZEEK_SPOOL_DIR:PATH=%{_localstatedir}/spool/zeek \
  -DZEEK_LOG_DIR:PATH=%{_localstatedir}/log/zeek \
..
make %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT
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
mv %{buildroot}/usr/lib/zeekctl/ZeekControl/ %{buildroot}%{python2_sitelib}/ZeekControl/
mv %{buildroot}/usr/lib/zeekctl/BroControl/ %{buildroot}%{python2_sitelib}/BroControl/
mv %{buildroot}/usr/lib/zeekctl/plugins %{buildroot}%{python2_sitelib}/ZeekControl/plugins

# Remove capstats, trace-summary, and pysubnettree
rm -f %{buildroot}/usr/bin/capstats
rm -f %{buildroot}/usr/bin/trace-summary
rm -f %{buildroot}%{python2_sitelib}/SubnetTree.*
rm -f %{buildroot}%{python2_sitelib}/_SubnetTree.*

# Python byte compile zeekctl module
%py_byte_compile %{__python2} %{buildroot}%{py_sitedir}

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
%{_bindir}/broctl
%{_bindir}/zeekctl
%{python2_sitelib}/BroControl
%{python2_sitelib}/ZeekControl
%{_mandir}/man8/zeekctl.8*
%{_mandir}/man1/trace-summary.1*

%dir %attr(-, zeek, zeek) %{_localstatedir}/log/zeek/
%dir %attr(-, zeek, zeek) %{_localstatedir}/spool/zeek/
%ghost %{_localstatedir}/log/zeek/*
%ghost %{_localstatedir}/spool/zeek/*

%dir %{_datadir}/zeek/zeekctl


# Needed if user moves the /var/spool/zeek directory elsewhere
%attr(-, zeek, zeek) %{_datadir}/zeekctl/scripts/


%changelog
