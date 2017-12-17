%global modname ConcurrentLogHandler
%global srcname concurrentloghandler
%global altname concurrent-log-handler

%if 0%{?fedora} || 0%{?epel} > 6
%bcond_without with_python3
%else
%bcond_with with_python3
%endif


Name:           python-%{srcname}
Version:        0.9.1
Release:        6%{?dist}
Summary:        Concurrent logging handler (drop-in replacement for RotatingFileHandler)

License:        ASL 2.0
URL:            https://pypi.python.org/pypi/ConcurrentLogHandler/
Source0:        https://pypi.python.org/packages/source/C/%{modname}/%{modname}-%{version}.tar.gz
# Upstream's setup.py tries to install tests and doc into /usr which is not what we want
Patch0:         %{modname}-0.8.6-testpath.patch

BuildArch:      noarch

%description
This module provides an additional log handler for Python's standard logging
package (PEP 282). This handler will write log events to log file which is
rotated when the log file reaches a certain size. Multiple processes can safely
write to the same log file concurrently.

%package -n python2-%{srcname}
Summary:        %{summary}
%{?python_provide:%python_provide python2-%{modname}}
%{?python_provide:%python_provide python2-%{srcname}}
%{?python_provide:%python_provide python2-%{altname}}
BuildRequires:  python2-devel python2-setuptools
BuildRequires:  python2-portalocker
Requires:       python2-portalocker

%description -n python2-%{srcname}
This module provides an additional log handler for Python's standard logging
package (PEP 282). This handler will write log events to log file which is
rotated when the log file reaches a certain size. Multiple processes can safely
write to the same log file concurrently.

Python 2 version.

%if %{with python3}
%package -n python3-%{srcname}
Summary:        %{summary}
%{?python_provide:%python_provide python3-%{modname}}
%{?python_provide:%python_provide python3-%{srcname}}
%{?python_provide:%python_provide python3-%{altname}}
BuildRequires:  /usr/bin/2to3
BuildRequires:  python3-devel python3-setuptools
BuildRequires:  python3-portalocker
Requires:       python3-portalocker

%description -n python3-%{srcname}
This module provides an additional log handler for Python's standard logging
package (PEP 282). This handler will write log events to log file which is
rotated when the log file reaches a certain size. Multiple processes can safely
write to the same log file concurrently.

Python 3 version.
%endif

%prep
%setup -qc
mv %{modname}-%{version} python2

pushd python2
%patch0 -p1
# Drop bundled portalocker
rm -rf src/portalocker.py
# Drop bundled egg
rm -rf src/*.egg-info
popd

%if %{with python3}
cp -a python2 python3
2to3 --write --nobackups python3
%endif

%build
pushd python2
  %py2_build
popd

%if %{with python3}
pushd python3
  %py3_build
popd
%endif

%install
pushd python2
  %py2_install
popd

%if %{with python3}
pushd python3
  %py3_install
popd
%endif

%check
pushd python2
  PYTHONPATH=%{buildroot}%{python2_sitelib} %{__python2} stresstest.py
popd

%if %{with python3}
pushd python3
  PYTHONPATH=%{buildroot}%{python3_sitelib} %{__python3} stresstest.py
popd
%endif

%files -n python2-%{srcname}
%license python2/LICENSE
%doc python2/README
%{python2_sitelib}/%{modname}-*.egg-info
%{python2_sitelib}/cloghandler.py*

%if %{with python3}
%files -n python3-%{srcname}
%license python3/LICENSE
%doc python3/README
%{python3_sitelib}/%{modname}-*.egg-info
%{python3_sitelib}/cloghandler.py
%{python3_sitelib}/__pycache__/cloghandler.*
%endif

%changelog
* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Mon Dec 19 2016 Miro Hrončok <mhroncok@redhat.com> - 0.9.1-3
- Rebuild for Python 3.6

* Tue Jul 19 2016 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.1-2
- https://fedoraproject.org/wiki/Changes/Automatic_Provides_for_Python_RPM_Packages

* Sun Mar 27 2016 Igor Gnatenko <i.gnatenko.brain@gmail.com> - 0.9.1-1
- Update to 0.9.1
- Add python3 subpackage
- Follow new packaging guidelines
- Run tests
- Unbundle portalocker
- Drop egg

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.8.7-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8.7-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8.7-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8.7-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Jul 18 2013 Dan Callaghan <dcallagh@redhat.com> - 0.8.7-1
- upstream bug fix release 0.8.7

* Tue Jul 09 2013 Dan Callaghan <dcallagh@redhat.com> - 0.8.6-1
- upstream bug fix release 0.8.6

* Wed Jun 26 2013 Dan Callaghan <dcallagh@redhat.com> - 0.8.4-10
- RHBZ#905286: don't release stream lock if already closed

* Thu May 16 2013 Dan Callaghan <dcallagh@redhat.com> - 0.8.4-9
- RHBZ#952929: ensure stream lock is closed
- RHBZ#858922: suppress exceptions in release

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8.4-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Sep 20 2012 Dan Callaghan <dcallagh@redhat.com> - 0.8.4-7
- RHBZ#858912: dont't flush log file if already closed

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8.4-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8.4-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Thu Oct 13 2011 Dan Callaghan <dcallagh@redhat.com> - 0.8.4-4
- add a comment about why testpath.patch is needed

* Wed Oct 12 2011 Dan Callaghan <dcallagh@redhat.com> - 0.8.4-3
- clean up spec a little more
- drop version from setuptools dependency as it is not needed

* Tue Oct 04 2011 Dan Callaghan <dcallagh@redhat.com> - 0.8.4-2
- clean up spec a little

* Tue Dec 14 2010 Bill Peck <bpeck@redhat.com> - 0.8.4-1
- initial version
