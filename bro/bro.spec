Name:             bro
Version:          2.6.3
Release:          1%{?dist}
Summary:          A Network Intrusion Detection System and Analysis Framework

License:          BSD
URL:              http://bro.org
Source0:          http://www.bro.org/downloads/%{name}-%{version}-minimal.tar.gz
Patch0:           https://github.com/zeek/zeek/commit/22f15b70.patch#/%{name}-%{version}-cmake-gnuinstalldirs.patch

Provides:         zeek
Requires:         bro-core = %{version}-%{release}

Requires:         broctl = 1:1.9
Requires:         bro-aux = 1:0.43
BuildRequires:    cmake >= 2.8.12

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
%package core
Summary:          The core bro installation without broctl
Requires:         libbroker = 1.1.2
BuildRequires:    libbroker-devel = 1.1.2
Requires:         caf = 0.16.3
BuildRequires:    caf-devel = 0.16.3
Requires:         bind-libs
BuildRequires:    bind-devel
Requires:         libmaxminddb0
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

BuildRequires:    binpac = 1:0.53
BuildRequires:    binpac-devel = 1:0.53
BuildRequires:    bifcl = 1:1.1
BuildRequires:    gcc-c++
BuildRequires:    openssl-devel
BuildRequires:    flex
BuildRequires:    bison >= 2.5
BuildRequires:    python2
BuildRequires:    sed

%description core
Bro is a powerful network analysis framework that is much different from the
typical IDS you may know.  While focusing on network security monitoring, Bro
provides a comprehensive platform for more general network traffic analysis as
well. Well grounded in more than 15 years of research, Bro has successfully
bridged the traditional gap between academia and operations since its
inception. Today, it is relied upon operationally in particular by many
scientific environments for securing their cyberinfrastructure. Bros user
community includes major universities, research labs, supercomputing centers,
and open-science communities.


%package devel
Summary:    The development headers for bro
Requires:   bro-core = %{version}-%{release}
Requires:   binpac-devel = 1:0.53
Requires:   libpcap-devel 
Requires:   libbroker-devel = 1.1.2
Requires:   caf-devel = 0.16.3
Requires:   bind-devel
Requires:   gperftools-devel
Requires:   openssl-devel

%description devel
This package contains the development headers needed to build new Bro plugins.

%prep
%setup -q -n %{name}-%{version}-minimal
%patch0 -p1

%build
mkdir build; cd build
%cmake \
  -DBRO_ROOT_DIR:PATH=%{_prefix} \
  -DPY_MOD_INSTALL_DIR:PATH=%{python2_sitelib} \
  -DBRO_SCRIPT_INSTALL_PATH:PATH=%{_datadir}/bro \
  -DBRO_ETC_INSTALL_DIR:PATH=%{_sysconfdir}/bro \
  -DENABLE_MOBILE_IPV6:BOOL=ON \
  -DBRO_DIST:PATH=%{_usrsrc}/%{name}-%{version}  \
  -DCMAKE_SKIP_RPATH:BOOL=ON \
  -DCAF_ROOT_DIR:PATH=%{_prefix} \
  -DINSTALL_AUX_TOOLS:BOOL=OFF \
  -DINSTALL_BROCTL:BOOL=OFF \
  -DBUILD_SHARED_LIBS:BOOL=ON \
  -DBinPAC_INCLUDE_DIR:PATH=%{_includedir} \
  -DBIFCL_EXE_PATH:PATH=%{_bindir}/bifcl \
  -DBINPAC_EXE_PATH:PATH=%{_bindir}/binpac \
  -DBROKER_ROOT_DIR:PATH=%{_prefix} \
  -DCAF_INCLUDE_DIRS:PATH=%{_includedir} \
  ..

%make_build

# # Gets the broker library on the ld path, needed to generate docs
# export LD_LIBRARY_PATH="${LD_LIBRARY_PATH}:%{buildroot}/build/aux/broker/lib/"
# make doc
# # Fix doc related rpmlint issues
# rm -rf %{_builddir}/%{name}-%{version}/build/doc/sphinx_output/html/.tmp
# rm -rf %{_builddir}/%{name}-%{version}/build/doc/sphinx_output/html/.buildinfo
# rm -rf %{_builddir}/%{name}-%{version}/build/doc/sphinx_output/html/_static/broxygen-extra.js
# find %{_builddir}/%{name}-%{version}/build/doc/ -size 0 -delete
# sed -i "s|\r||g" %{_builddir}/%{name}-%{version}/build/doc/sphinx_output/html/objects.inv
# f="%{_builddir}/%{name}-%{version}/build/doc/sphinx_output/html/objects.inv"
# iconv --from=ISO-8859-1 --to=UTF-8 $f > $f.new && \
# touch -r $f $f.new && \
# mv $f.new $f

################################################################################
%install
cd build
%make_install
#
# # Install scripts
# pushd scripts
# %{__install} -d -m 755 %{buildroot}%{_datadir}/bro/scripts
# popd
#
# # The signature samples should go into a seperate sub-package if possible
# # Install example signatures, site policy
# %{__install} -D -d -m 755 %{buildroot}%{_localstatedir}/lib/bro/site
# %{__install} -D -d -m 755 %{buildroot}%{_localstatedir}/lib/bro/host


#
# # Remove devel, junk, and zero length files
# find "%{buildroot}%{_prefix}" -iname "*.la" -delete;
# find "%{buildroot}" -iname "*.log" -delete;
# rm -rf %{buildroot}%{_includedir}/binpac.h.in


################################################################################
%check
ctest -V %{?_smp_mflags}


################################################################################
%files
%doc CHANGES NEWS README VERSION
%license COPYING

################################################################################
%files core
%doc CHANGES NEWS README VERSION
%license COPYING
%caps(cap_net_admin,cap_net_raw=pie) %{_bindir}/bro
%{_bindir}/bro-config
%{_mandir}/man8/bro.8*
%dir %{_datadir}/bro/
%{_datadir}/bro/base/
%{_datadir}/bro/broxygen/
%{_datadir}/bro/policy/
%config(noreplace) %{_datadir}/bro/site/local.bro

%files devel
%doc CHANGES NEWS README VERSION
%license COPYING
%dir %{_includedir}/bro
%{_includedir}/bro/*
%dir %{_datadir}/bro/cmake
%{_datadir}/bro/cmake/*

################################################################################
%changelog
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
