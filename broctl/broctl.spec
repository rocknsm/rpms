Name:           broctl
Version:        1.9
Release:        1%{?dist}
Epoch:          1
Summary:        Tool for managing Zeek deployments.

License:        BSD
URL:            https://github.com/zeek/broctl
Source0:        https://www.zeek.org/downloads/%{name}-%{version}.tar.gz
Source1:        bro.service

BuildRequires:  cmake >= 2.6.3
BuildRequires:  gcc-c++
BuildRequires:  python2-devel
BuildRequires:  capstats >= 0.26
BuildRequires:  trace-summary >= 0.88
BuildRequires:  systemd
BuildRequires:  swig
BuildRequires:  libpcap-devel
BuildRequires:  bro-core = 2.6.3
BuildRequires:  libbroker-python = 1.1.2

Requires:       bro-core = 2.6.3
Requires:       libbroker-python = 1.1.2
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
BroControl is an interactive interface for managing a Bro installation which
allows you to, e.g., start/stop the monitoring or update its configuration.

%prep
%setup -q

# Fix the hard-coded paths in BroControl options
sed -E -i.orig '
  /("LibDir"|"PluginBroDir")/s|/lib|%{_libdir}|;
  /LibDirInternal/s|/lib/broctl|%{python2_sitelib}/BroControl|;
  s|(%{_exec_prefix})+||
' BroControl/options.py

# Shebang
sed -i -e '1i#! /usr/bin/bash' bin/set-bro-path bin/helpers/to-bytes.awk

%build
mkdir build; cd build
%cmake \
  -DBRO_ROOT_DIR=%{_prefix} \
  -DBRO_ETC_INSTALL_DIR=%{_sysconfdir}/bro \
  -DBRO_SCRIPT_INSTALL_PATH=%{_datadir}/bro \
  -DPY_MOD_INSTALL_DIR=%{python2_sitelib} \
  -DBRO_LOCAL_STATE_DIR:PATH=%{_localstatedir} \
  -DBRO_SPOOL_DIR:PATH=%{_localstatedir}/spool/bro \
  -DBRO_LOG_DIR:PATH=%{_localstatedir}/log/bro \
..
make %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT
%make_install

# Install service file
%{__install} -D -c -m 644 %{SOURCE1} %{buildroot}%{_unitdir}/bro.service

# Install config
%{__install} -d -m 755 %{buildroot}%{_sysconfdir}/bro

# Create log dirs
%{__install} -d -m 755 %{buildroot}%{_localstatedir}/log/bro
%{__install} -d -m 755 %{buildroot}%{_localstatedir}/log/bro/archive
%{__install} -d -m 755 %{buildroot}%{_localstatedir}/log/bro/sorted-logs
%{__install} -d -m 755 %{buildroot}%{_localstatedir}/log/bro/stats

# Create spool dir
%{__install} -d -m 755 %{buildroot}%{_localstatedir}/spool/bro
%{__install} -d -m 755 %{buildroot}%{_localstatedir}/spool/bro/tmp

# Fix broctl python location
mv %{buildroot}/usr/lib/broctl/BroControl/ %{buildroot}%{python2_sitelib}/BroControl/
mv %{buildroot}/usr/lib/broctl/plugins %{buildroot}%{python2_sitelib}/BroControl/plugins

# Remove capstats, trace-summary, and pysubnettree
rm -f %{buildroot}/usr/bin/capstats
rm -f %{buildroot}/usr/bin/trace-summary
rm -f %{buildroot}%{python2_sitelib}/SubnetTree.*
rm -f %{buildroot}%{python2_sitelib}/_SubnetTree.*

# Python byte compile broctl module
%py_byte_compile %{__python2} %{buildroot}%{py_sitedir}

################################################################################
%pre
getent group bro >/dev/null || groupadd -r bro
getent passwd bro >/dev/null || \
    useradd -r -g bro -d %{_localstatedir}/lib/bro/ -s /sbin/nologin \
    -c "System account for Bro service" bro

exit 0

################################################################################
%post
%systemd_post bro.service

exit 0

################################################################################
%preun
%systemd_preun bro.service

################################################################################
%postun
%systemd_postun bro.service


%files
%doc

%dir %{_sysconfdir}/bro
%config(noreplace) %{_sysconfdir}/bro/broctl.cfg
%config(noreplace) %{_sysconfdir}/bro/node.cfg
%config(noreplace) %{_sysconfdir}/bro/networks.cfg
%{_unitdir}/bro.service
%dir %{_datadir}/broctl
%{_datadir}/bro/broctl/*.bro
%{_bindir}/broctl
%{python2_sitelib}/BroControl
%{_mandir}/man8/broctl.8*
%{_mandir}/man1/trace-summary.1*

%dir %attr(-, bro, bro) %{_localstatedir}/log/bro/
%dir %attr(-, bro, bro) %{_localstatedir}/spool/bro/
%ghost %{_localstatedir}/log/bro/*
%ghost %{_localstatedir}/spool/bro/*

%dir %{_datadir}/bro/broctl


# Needed if user moves the /var/spool/bro directory elsewhere
%attr(-, bro, bro) %{_datadir}/broctl/scripts/


%changelog
