%global BIFCL_VER 1:1.2
%global BINPAC_VER 1:0.55.1
%global BROKER_VER 1.3.3
%global CAF_VER 0.17.5
%global ZEEKAUX_VER 0.44
%global ZEEKCTL_VER 2.1.0

%if 0%{?rhel} < 8
%global scl devtoolset-8
%global scl_prefix devtoolset-8-
%global scl_enable cat << EOSCL | scl enable %{scl} -
%global scl_disable EOSCL
%endif

Name:             zeek
Version:          3.1.3
Release:          1%{?dist}
Summary:          A Network Intrusion Detection System and Analysis Framework

License:          BSD
URL:              http://bro.org
Source0:          https://download.zeek.org/%{name}-%{version}-minimal.tar.gz
Source1:          https://github.com/zeek/paraglob/archive/v0.4.1.tar.gz#/paraglob-0.4.1.tar.gz
Patch0:           https://github.com/zeek/zeek/compare/release/3.1...dcode:topic/dcode/gnuinstalldirs.patch#/01-%{name}-%{version}-gnu-install-dirs.patch
Patch1:           https://patch-diff.githubusercontent.com/raw/zeek/zeek/pull/954.patch#/02-%{name}-%{version}-bzar-dcerpc-constants.patch

Provides:         bro = %{version}
Obsoletes:        bro < %{version}

Requires:         zeek-core = %{version}-%{release}
Requires:         zeekctl >= %{ZEEKCTL_VER}
Requires:         zeek-aux >= %{ZEEKAUX_VER}

%if 0%{?rhel} < 8
BuildRequires:    cmake3  >= 3.0.0
%global cmake %cmake3
%global ctest /usr/bin/ctest3
%else
BuildRequires:    cmake   >= 3.0.0
%global ctest /usr/bin/ctest
%endif 


%description
Zeek is an open-source, Unix-based Network Intrusion Detection System (NIDS)
that passively monitors network traffic and looks for suspicious activity.
Zeek detects intrusions by first parsing network traffic to extract its
application-level semantics and then executing event-oriented analyzers that
compare the activity with patterns deemed troublesome. Its analysis includes
detection of specific attacks (including those defined by signatures, but also
those defined in terms of events) and unusual activities (e.g., certain hosts
connecting to certain services, or patterns of failed connection attempts).

################################################################################

%package core
Summary:          The core zeek installation (without zeekctl, zeek-aux, or develpment files).
Requires:         libbroker = %{BROKER_VER}
BuildRequires:    libbroker-devel = %{BROKER_VER}
Requires:         caf >= %{CAF_VER}
BuildRequires:    caf-devel >= %{CAF_VER}
Requires:         bind-libs
BuildRequires:    bind-devel
Requires:         libmaxminddb
BuildRequires:    libmaxminddb-devel
%ifnarch s390 s390x
Requires:         gperftools-libs
BuildRequires:    gperftools-devel
%endif
Requires:         libpcap
BuildRequires:    libpcap-devel
Requires:         openssl
BuildRequires:    openssl-devel
Requires:         zlib
Requires:         krb5-libs

BuildRequires:    binpac = %{BINPAC_VER}
BuildRequires:    binpac-devel = %{BINPAC_VER}
BuildRequires:    bifcl = %{BIFCL_VER}
BuildRequires:    %{?scl_prefix}gcc-c++ >= 8
BuildRequires:    openssl-devel
BuildRequires:    flex
BuildRequires:    bison >= 2.5
BuildRequires:    python3-devel
BuildRequires:    sed
BuildRequires:    git
BuildRequires:    krb5-devel

Provides:         bro-core = %{version}
Obsoletes:        bro-core < %{version}

%description core
Zeek is a powerful network analysis framework that is much different from the
typical IDS you may know.  While focusing on network security monitoring, Zeek
provides a comprehensive platform for more general network traffic analysis as
well. Well grounded in more than 15 years of research, Zeek has successfully
bridged the traditional gap between academia and operations since its
inception. Today, it is relied upon operationally in particular by many
scientific environments for securing their cyberinfrastructure. Zeek's user
community includes major universities, research labs, supercomputing centers,
and open-science communities.


%package devel
Summary:    The development headers for Zeek
Requires:   zeek-core = %{version}-%{release}
Requires:   binpac-devel = %{BINPAC_VER}
Requires:   libpcap-devel
Requires:   libbroker-devel = %{BROKER_VER}
Requires:   caf-devel >= %{CAF_VER}
Requires:   python3-devel
Requires:   krb5-devel
Requires:   bind-devel
Requires:   gperftools-devel
Requires:   openssl-devel

Provides:   bro-devel = %{version}
Obsoletes:  bro-devel < %{version}

%description devel
This package contains the development headers needed to build new Zeek plugins.

################################################################################
%prep
%autosetup -n %{name}-%{version}-minimal -S git

# Temporary hack and patch
cd aux/paraglob
tar zxf %{SOURCE1} --strip-components 1
sed -i '/project(paraglob)/a include(GNUInstallDirs)' CMakeLists.txt
sed -i 's/${CMAKE_INSTALL_PREFIX}\/lib/${CMAKE_INSTALL_LIBDIR}/' CMakeLists.txt
sed -i 's/DESTINATION include/DESTINATION ${CMAKE_INSTALL_INCLUDEDIR}/' CMakeLists.txt
sed -i 's/DESTINATION lib/DESTINATION ${CMAKE_INSTALL_LIBDIR}/' src/CMakeLists.txt

################################################################################
%build
mkdir build; cd build
%{?scl_enable} 
%cmake \
  -DZEEK_ROOT_DIR:PATH=%{_prefix} \
  -DPY_MOD_INSTALL_DIR:PATH=%{python3_sitelib} \
  -DPYTHON_EXECUTABLE:PATH=%{python3} \
  -DZEEK_SCRIPT_INSTALL_PATH:PATH=%{_datadir}/%{name} \
  -DZEEK_ETC_INSTALL_DIR:PATH=%{_sysconfdir}/%{name} \
  -DENABLE_MOBILE_IPV6:BOOL=ON \
  -DZEEK_DIST:PATH=%{_usrsrc}/%{name}-%{version}  \
  -DCMAKE_SKIP_RPATH:BOOL=ON \
  -DCAF_ROOT_DIR:PATH=%{_prefix} \
  -DINSTALL_AUX_TOOLS:BOOL=OFF \
  -DINSTALL_ZEEKCTL:BOOL=OFF \
  -DBUILD_SHARED_LIBS:BOOL=ON \
  -DBinPAC_INCLUDE_DIR:PATH=%{_includedir} \
  -DBIFCL_EXE_PATH:PATH=%{_bindir}/bifcl \
  -DBINPAC_EXE_PATH:PATH=%{_bindir}/binpac \
  -DBROKER_ROOT_DIR:PATH=%{_prefix} \
  -DCAF_INCLUDE_DIRS:PATH=%{_includedir} \
  ..
%{?scl_disable}

%{?scl_enable} 
%make_build
%{?scl_disable}

################################################################################
%install
cd build

%{?scl_enable} 
%make_install
%{?scl_disable}

################################################################################
%check
cd build
%{?scl_enable} 
%ctest -V %{?_smp_mflags}
%{?scl_disable}

################################################################################
%files
%doc CHANGES NEWS README VERSION
%license COPYING

################################################################################
%files core
%doc CHANGES NEWS README VERSION
%license COPYING
%caps(cap_net_admin,cap_net_raw=pie) %{_bindir}/%{name}
%{_bindir}/%{name}-config
%{_bindir}/paraglob-test
%{_bindir}/%{name}-wrapper
%{_mandir}/man8/%{name}.8*
%dir %{_datadir}/%{name}/
%{_datadir}/%{name}/base/
%{_datadir}/%{name}/zeekygen/
%{_datadir}/%{name}/policy/
%{_datadir}/%{name}/test-all-policy.zeek
%config(noreplace) %{_datadir}/%{name}/site/local.zeek

%files devel
%doc CHANGES NEWS README VERSION
%license COPYING
%dir %{_includedir}/%{name}
%{_includedir}/%{name}/*
%dir %{_datadir}/%{name}/cmake
%{_datadir}/%{name}/cmake/*
%{_includedir}/paraglob/
%{_libdir}/libparaglob.a

################################################################################
%changelog
* Wed May 20 2020 Derek Ditch <derek@rocknsm.io> 3.1.3-1
- Bump version for latest feature release
- Switched completely to python3
- Switched build to use cmake3 and gcc >= 8

* Mon Dec 16 2019 Derek Ditch <derek@rocknsm.io> 3.0.1-1
- Version bump for upstream bugfixes

* Tue Sep 24 2019 Derek Ditch <derek@rocknsm.io> 3.0.0-1
- New analzers for NTP and MQTT
- Extended analyzers for DNS, RDP, SMB, and TLS
- Support for logging in UTF-8
- Extensions to scripting language, for example closures
- Renames to transition from bro to zeek
- See https://blog.zeek.org/2019/09/zeek-300.html for more details

* Mon Sep 16 2019 Derek Ditch <derek@rocknsm.io> 3.0.0-0rc2
- Bump to version 3.0.0 RC2

* Thu Sep 5 2019 Derek Ditch <derek@rocknsm.io> 2.6.4-1
- Bump to version 2.6.4 to fix NTLM bug

* Fri Aug 23 2019 Derek Ditch <derek@rocknsm.io> 2.6.3-1
- Bump to version 2.6.3 upstream
- Version locked lib dependencies

* Thu Feb 14 2019 Derek Ditch <derek@rocknsm.io> 2.6.1-1
- Bumped version to upstream 2.6.1
- Split out all non-core and non-devel packages to their own RPMs

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
