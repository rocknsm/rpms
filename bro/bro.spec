Name:             bro
Version:          2.5.5
Release:          1%{?dist}
Summary:          A Network Intrusion Detection System and Analysis Framework

License:          BSD
URL:              http://bro.org
Source0:          http://www.bro.org/downloads/%{name}-%{version}.tar.gz
Source1:          bro.service
#Source2:          bro-logrotate.conf
# Fix for the usage of configure with cmake and rpm build tools
Patch0:           %{name}-%{version}-configure.patch
# The aux tools are separate packages. No need to build them.
Patch1:           %{name}-%{version}-broctl-disable-aux.patch
# Adjust the paths
Patch2:           %{name}-%{version}-cmake-devel.patch
# Fix for sphinx on EL7
Patch3:           %{name}-%{version}-sphinx-bro-ext.patch

Requires:         bro-core = %{version}-%{release}
Requires:         broctl = %{version}-%{release}
Requires:         broccoli = %{version}-%{release}

%description
Bro is an open-source, Unix-based Network Intrusion Detection System (NIDS)
that passively monitors network traffic and looks for suspicious activity.
Bro detects intrusions by first parsing network traffic to extract is
application-level semantics and then executing event-oriented analyzers that
compare the activity with patterns deemed troublesome. Its analysis includes
detection of specific attacks (including those defined by signatures, but also
those defined in terms of events) and unusual activities (e.g., certain hosts
connecting to certain services, or patterns of failed connection attempts).

################################################################################
%package -n bro-core
Summary:        The core bro installation without broctl
Requires:       bind-libs
Requires:       GeoIP
%ifnarch s390 s390x
Requires:       gperftools
%endif
Requires:       libpcap
%if 0%{?fedora} >= 26
Requires:       compat-openssl10
%else
Requires:       openssl
%endif
Requires:       zlib

BuildRequires:  bind-devel
BuildRequires:  bison
BuildRequires:  cmake
BuildRequires:  flex
BuildRequires:  GeoIP-devel
BuildRequires:  gcc-c++
%ifnarch s390 s390x
BuildRequires:  gperftools-devel
%endif
BuildRequires:  libpcap-devel
%if 0%{?fedora} >= 26
BuildRequires:  compat-openssl10-devel
%else
BuildRequires:  openssl-devel
%endif
BuildRequires:  python2-devel
BuildRequires:  swig
BuildRequires:  zlib-devel

%description -n bro-core
Bro is a powerful network analysis framework that is much different from the
typical IDS you may know.  While focusing on network security monitoring, Bro
provides a comprehensive platform for more general network traffic analysis as
well. Well grounded in more than 15 years of research, Bro has successfully
bridged the traditional gap between academia and operations since its
inception. Today, it is relied upon operationally in particular by many
scientific environments for securing their cyberinfrastructure. Bro's user
community includes major universities, research labs, supercomputing centers,
and open-science communities.

################################################################################
%package -n bro-devel
Summary:        Compile-time generated source files needed to build bro packages

Requires:  cmake
Requires:  bro-core = %{version}-%{release}

%description -n bro-devel
Installs the compile-time generated files known as BRODIST needed to build bro
packages and plugins. The files can be find in /usr/src/%{name}-%{version}.

################################################################################
%package -n binpac
Summary:        A language for protocol parsers

%description -n binpac
BinPAC is a high level language for describing protocol parsers and generates
C++ code. It is currently maintained and distributed with the Bro Network
Security Monitor distribution, however, the generated parsers may be used
with other programs besides Bro.

################################################################################
%package -n binpac-devel
Summary:        Development file for binpac
Requires:       binpac = %{version}-%{release}
Provides:       binpac-static = %{version}-%{release}

%description -n binpac-devel
This package contains the header files for binpac.

################################################################################
%package -n broctl
Summary:          A control tool for bro
Buildarch:        noarch
BuildRequires:    python-devel
BuildRequires:    systemd
BuildRequires:    pysubnettree
BuildRequires:    trace-summary
BuildRequires:    capstats

Requires:         python2
Requires:         bash
Requires:         pysubnettree
Requires:         trace-summary
Requires:         capstats
Requires:         broccoli = %{version}-%{release}
Requires:         python2-broccoli = %{version}-%{release}
Requires:         bro-core = %{version}-%{release}

Requires(pre):    /usr/bin/getent
Requires(pre):    /usr/sbin/groupadd
Requires(pre):    /usr/sbin/useradd
Requires(post):   systemd
Requires(preun):  systemd
Requires(postun): systemd

%description -n broctl
BroControl is an interactive interface for managing a Bro installation which
allows you to, e.g., start/stop the monitoring or update its configuration.

################################################################################
%package -n broccoli
Summary:          The bro client communication library
BuildRequires:    flex
BuildRequires:    bison
BuildRequires:    cmake
BuildRequires:    libpcap-devel
Requires:         libpcap
%if 0%{?fedora} >= 26
BuildRequires:    compat-openssl10-devel
Requires:         compat-openssl10
%else
BuildRequires:    openssl-devel
Requires:         openssl
%endif

%description -n broccoli
Broccoli is the "Bro client communications library". It allows you to create
client sensors for the Bro intrusion detection system. Broccoli can speak a
good subset of the Bro communication protocol, in particular, it can receive
Bro IDs, send and receive Bro events, and send and receive event requests
to/from peering Bros. You can currently create and receive values of pure
types like integers, counters, timestamps, IP addresses, port numbers,
booleans, and strings.

################################################################################
%package -n broccoli-devel
Summary:          Development file for broccoli

Requires:         bro = %{version}-%{release}
Requires:         pkgconfig

%description -n broccoli-devel
This package contains the header files for broccoli.

################################################################################
%package -n python2-broccoli
%{?python_provide:%python_provide python2-broccoli}
Summary:          Python bindings for bro

BuildRequires:    python2-devel

Requires:         broccoli = %{version}-%{release}
Requires:         pysubnettree
Requires:         trace-summary
Requires:         capstats

%description -n python2-broccoli
This Python module provides bindings for Broccoli, Bro’s client communication
library.

################################################################################
%package doc
Summary:          Documentation for bro

BuildRequires:    python-sphinx
BuildRequires:    doxygen
BuildRequires:    rsync

%description doc
This package contains the documentation for bro.

################################################################################
%prep
%setup -q

%patch0 -p1 -b .configure
%patch1 -p1 -b .cmake
%patch2 -p1 -b .cmake
%patch3 -p1 -b .sphinx

# Fix the hard-coded paths in BroControl options
sed -E -i.orig '
  /("LibDir"|"PluginBroDir")/s|/lib|%{_libdir}|;
  /LibDirInternal/s|/lib/broctl|%{python2_sitelib}/BroControl|;
  s|(%{_exec_prefix})+||
' aux/broctl/BroControl/options.py

# Shebang
sed -i -e '1i#! /usr/bin/bash' aux/broctl/bin/set-bro-path aux/broctl/bin/helpers/to-bytes.awk

################################################################################
%build
%configure \
    --prefix=%{_prefix} \
    --libdir=%{_libdir} \
    --localstatedir=%{_localstatedir} \
    --spooldir=%{_localstatedir}/spool/bro \
    --logdir=%{_localstatedir}/log/bro \
    --conf-files-dir=%{_sysconfdir}/bro \
    --python-install-dir=%{python2_sitelib} \
    --plugindir=%{_libdir}/bro/plugins \
    --distdir=%{_usrsrc}/%{name}-%{version} \
    --disable-rpath \
    --enable-debug \
    --enable-mobile-ipv6 \
    --enable-binpac
make %{?_smp_mflags}
make doc
# Fix doc related rpmlint issues
rm -rf %{_builddir}/%{name}-%{version}/build/doc/sphinx_output/html/.tmp
rm -rf %{_builddir}/%{name}-%{version}/build/doc/sphinx_output/html/.buildinfo
rm -rf %{_builddir}/%{name}-%{version}/build/doc/sphinx_output/html/_static/broxygen-extra.js
find %{_builddir}/%{name}-%{version}/build/doc/ -size 0 -delete
sed -i "s|\r||g" %{_builddir}/%{name}-%{version}/build/doc/sphinx_output/html/objects.inv
f="%{_builddir}/%{name}-%{version}/build/doc/sphinx_output/html/objects.inv"
iconv --from=ISO-8859-1 --to=UTF-8 $f > $f.new && \
touch -r $f $f.new && \
mv $f.new $f

################################################################################
%install
make install DESTDIR=%{buildroot} INSTALL="install -p"

# Create bro-devel directory
%{__install} -d -m 755 %{buildroot}%{_usrsrc}/%{name}-%{version}

# Copy over devel files, skipping docs and intermediate objects
mkdir -p %{buildroot}%{_usrsrc}/%{name}-%{version}/
rsync -rptlv \
    --exclude=*.o \
    --exclude=*.a \
    --exclude=*.so \
    --exclude=build/doc \
    --exclude=build/man \
    --exclude=.tmp \
    --exclude=testing \
    %{_builddir}/%{name}-%{version}/ %{buildroot}%{_usrsrc}/%{name}-%{version}/

# Override binaries with symlinks
ln -sf %{_libdir}/libbroccoli.so.5.1.0 %{buildroot}%{_usrsrc}/%{name}-%{version}/build/aux/broccoli/src/libbroccoli.so.5.1.0
ln -sf %{_bindir}/bro %{buildroot}%{_usrsrc}/%{name}-%{version}/build/src/bro
ln -sf %{_bindir}/bro-cut %{buildroot}%{_usrsrc}/%{name}-%{version}/build/aux/bro-aux/bro-cut/bro-cut
ln -sf %{_bindir}/binpac %{buildroot}%{_usrsrc}/%{name}-%{version}/build/aux/binpac/src/binpac

# Change the paths to the installed locations on non-executable files
find %{buildroot}%{_usrsrc}/%{name}-%{version}/ \
    -type f \
    ! -perm -111 \
    -exec sed -i 's|%{_builddir}/%{name}-%{version}|%{_usrsrc}/%{name}-%{version}|g' {} \;

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

# Install scripts
pushd scripts
%{__install} -d -m 755 %{buildroot}%{_datadir}/bro/scripts
popd

# The signature samples should go into a seperate sub-package if possible
# Install example signatures, site policy
%{__install} -D -d -m 755 %{buildroot}%{_localstatedir}/lib/bro/site
%{__install} -D -d -m 755 %{buildroot}%{_localstatedir}/lib/bro/host

# Fix broctl python location
mv %{buildroot}/usr/lib/broctl/BroControl/ %{buildroot}%{python2_sitelib}/BroControl/
mv %{buildroot}/usr/lib/broctl/plugins %{buildroot}%{python2_sitelib}/BroControl/plugins

# Move static library to default location
%if 0%{?__isa_bits} == 64
mkdir -p %{buildroot}%{_libdir}
mv %{buildroot}/usr/lib/libbinpac.a %{buildroot}%{_libdir}/libbinpac.a
%endif

# Remove devel, junk, and zero length files
find "%{buildroot}%{_prefix}" -iname "*.la" -delete;
find "%{buildroot}" -iname "*.log" -delete;
rm -rf %{buildroot}%{_includedir}/binpac.h.in

################################################################################
%pre -n broctl
getent group bro >/dev/null || groupadd -r bro
getent passwd bro >/dev/null || \
    useradd -r -g bro -d %{_localstatedir}/lib/bro/ -s /sbin/nologin \
    -c "System account for Bro service" bro

exit 0

################################################################################
%post -n broctl
%systemd_post bro.service

exit 0

################################################################################
%preun -n broctl
%systemd_preun bro.service

################################################################################
%postun -n broctl
%systemd_postun bro.service

################################################################################
%post -n broccoli -p /sbin/ldconfig
%if ( 0%{?_undocumented_hack_closes_scriptlets} )
%postun
%endif

################################################################################
%postun -n broccoli -p /sbin/ldconfig
%if ( 0%{?_undocumented_hack_closes_scriptlets} )
%postun
%endif


################################################################################
%check
make test

################################################################################
%files
%doc CHANGES NEWS README VERSION
%license COPYING

################################################################################
%files -n bro-core
%doc CHANGES NEWS README VERSION
%license COPYING
%caps(cap_net_admin,cap_net_raw=pie) %{_bindir}/bro
%{_bindir}/bro-config
%{_bindir}/bro-cut
%{_mandir}/man1/bro-cut.1*
%{_mandir}/man8/bro.8*
%config(noreplace) %{_datadir}/bro/site/local.bro
%{_datadir}/bro/

################################################################################
%files -n bro-devel
%{_usrsrc}/%{name}-%{version}/

################################################################################
%files -n binpac
%doc CHANGES README
%license COPYING
%{_bindir}/binpac

################################################################################
%files -n binpac-devel
%{_includedir}/binpac*.h
%{_libdir}/libbinpac.a

################################################################################
%files -n broctl
%config(noreplace) %{_sysconfdir}/bro/broctl.cfg
%config(noreplace) %{_sysconfdir}/bro/node.cfg
%config(noreplace) %{_sysconfdir}/bro/networks.cfg
%{_unitdir}/bro.service
%{_datadir}/broctl/
%{_bindir}/broctl
%{python2_sitelib}/BroControl
%{_mandir}/man8/broctl.8*

%dir %{_localstatedir}/lib/bro/
%ghost %{_localstatedir}/lib/bro/*

%dir %attr(-, bro, bro) %{_localstatedir}/log/bro/
%dir %attr(-, bro, bro) %{_localstatedir}/spool/bro/
%ghost %{_localstatedir}/log/bro/*
%ghost %{_localstatedir}/spool/bro/*

# Needed if user moves the /var/spool/bro directory elsewhere
%attr(-, bro, bro) %{_datadir}/broctl/scripts/

################################################################################
%files -n broccoli
%config(noreplace) %{_sysconfdir}/bro/broccoli.conf
%{_libdir}/libbroccoli.so.*

################################################################################
%files -n broccoli-devel
%{_bindir}/broccoli-config
%{_libdir}/libbroccoli.so
%{_includedir}/broccoli.h
%exclude %{_libdir}/libbroccoli.a

################################################################################
%files -n python2-broccoli
%{python2_sitelib}/*broccoli*

################################################################################
%files doc
%doc doc/README
%doc build/doc/sphinx_output/html
%license doc/LICENSE

################################################################################
%changelog
* Thu Feb 15 2018 Derek Ditch <derek@rocknsm.io> 2.5.3-1
- Security fix for binpac, bump to 2.5.3 
- Remove linux capabilities from service file. Didn't work.

* Sat Jan 27 2018 Derek Ditch <derek@rocknsm.io> 2.5.2-4
- Fixes permissions on spool and log dirs
- Adds net_admin, net_raw, and sys_nice caps to service file.

* Mon Nov 20 2017 Derek Ditch <derek@rocknsm.io> 2.5.2-3
- Adds bro system user and group in broctl \%post script
- Fixes bug in broccoli \%post scriplets to run ldconfig

* Tue Nov 7 2017 Derek Ditch <derek@rocknsm.io> 2.5.2-2
- Moved licenses from doc to license
- Removed jemalloc in favor of gperftools to fix crash

* Mon Oct 16 2017 Derek Ditch <derek@rocknsm.io> 2.5.2-1
- Update to latest upstream version 2.5.2
- 2.5.2 is a security update

* Tue Oct 10 2017 Derek Ditch <derek@rocknsm.io> 2.5.1-1
- Added plugin configure option for bro-devel package
- Fixed bro-devel package for use with plugins
- Update to latest upstream version 2.5.1
- Removed logrotate configuration; handled by broctl
- Split out bro-core package for standlone bro installations
- Create bro-devel package
- Patched bro sphinx ext for epel7

* Sat Aug 19 2017 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 2.4.1-7
- Python 2 binary package renamed to python2-bro
  See https://fedoraproject.org/wiki/FinalizingFedoraSwitchtoPython3

* Wed Aug 02 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.4.1-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.4.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.4.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Tue Jul 19 2016 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.4.1-3
- https://fedoraproject.org/wiki/Changes/Automatic_Provides_for_Python_RPM_Packages

* Wed Feb 03 2016 Fedora Release Engineering <releng@fedoraproject.org> - 2.4.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Sun Sep 13 2015 Fabian Affolter <mail@fabian-affolter.ch> - 2.4.1-1
- Update to latest upstream version 2.4.1

* Sun Aug 30 2015 Fabian Affolter <mail@fabian-affolter.ch> - 2.3.2-7
- Rebuild for libjemalloc

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.3.2-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Thu Jun 11 2015 Dan Horák <dan[at]danny.cz> - 2.3.2-5
- gperftools not available on s390(x)

* Thu May 28 2015 Fabian Affolter <mail@fabian-affolter.ch> - 2.3.2-4
- Fix requirements (rhbz#1220801)

* Tue Apr 28 2015 Peter Robinson <pbrobinson@fedoraproject.org> 2.3.2-3
- Fix NVR requires

* Mon Apr 20 2015 Marcin Juszkiewicz <mjuszkiewicz@redhat.com> - 2.3.2-2
- x86-64 is not the only one 64-bit architecture in Fedora (rhbz#1213420)

* Tue Mar 03 2015 Fabian Affolter <mail@fabian-affolter.ch> - 2.3.2-1
- Update to latest upstream version 2.3.2

* Fri Jan 23 2015 Fabian Affolter <mail@fabian-affolter.ch> - 2.3.1-1
- Update to latest upstream version 2.3.1 (rhbz#1140090)

* Fri Aug 15 2014 Fabian Affolter <mail@fabian-affolter.ch> - 2.3-1
- Introduce logrotate
- Move docs, python bindings, broctl, and broccoli to subpackage
- Update systemd macros (rhbz#850051)
- Add ghost (rhbz#656552)
- capstats, trace-summary, pysubnettree, btest, and binpac are separate packages
- Update to latest upstream version 2.3 (rhbz#979726)

* Fri Aug 15 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.5.1-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Thu Jul 31 2014 Yaakov Selkowitz <yselkowi@redhat.com> - 1.5.1-11
- Fix FTBFS with -Werror=format-security (#1037005, #1106016)

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.5.1-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.5.1-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild
- BR: systemd-units for %%{_unitdir} macro definition

* Wed Jul 17 2013 Petr Pisar <ppisar@redhat.com> - 1.5.1-8
- Perl 5.18 rebuild

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.5.1-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Jul 18 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.5.1-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Wed Apr 18 2012 Jon Ciesla <limburgher@gmail.com> - 1.5.1-5
- Migrate to systemd, BZ 771767.

* Thu Jan 12 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.5.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Feb 07 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.5.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Sep 29 2010 jkeating - 1.5.1-2
- Rebuilt for gcc bug 634757

* Wed Sep  8 2010 Daniel Kopecek <dkopecek@redhat.com> - 1.5.1-1
- update to new upstream version

* Tue Aug 25 2009 Tomas Mraz <tmraz@redhat.com> - 1.4-0.6.20080804svn
- rebuilt with new openssl

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4-0.5.20080804svn
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Mon Feb 23 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4-0.4.20080804svn
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Thu Jan 15 2009 Tomas Mraz <tmraz@redhat.com> - 1.4-0.3.20080804svn
- rebuild with new openssl

* Tue Aug 26 2008 Daniel Kopecek <dkopecek@redhat.com> - 1.4-0.2.20080804svn
- Added patch to prevent collision with the internal
  variable in Autoconf 2.62. Thanks to skasal@redhat.com.

* Wed May  7 2008 Daniel Kopecek <dkopecek@redhat.com> - 1.4-0.1.20080804svn
- Initial build.
