%global modname portalocker

%if 0%{?fedora} || 0%{?epel} > 6
%bcond_without with_python3
%else
%bcond_with with_python3
%endif

Name:           python-%{modname}
Version:        1.0.1
Release:        3%{?dist}
Summary:        Library to provide an easy API to file locking

License:        Python
URL:            https://github.com/WoLpH/portalocker
Source0:        %{url}/archive/v%{version}/%{modname}-%{version}.tar.gz

BuildArch:      noarch

%description
%{summary}.

%package -n python2-%{modname}
Summary:        %{summary}
%{?python_provide:%python_provide python2-%{modname}}
BuildRequires:  python2-devel
BuildRequires:  python2-setuptools
BuildRequires:  python2-pytest
BuildRequires:  python2-pytest-runner

%description -n python2-%{modname}
%{summary}.

Python 2 version.

%if %{with python3}
%package -n python3-%{modname}
Summary:        %{summary}
%{?python_provide:%python_provide python3-%{modname}}
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
BuildRequires:  python3-pytest
BuildRequires:  python3-pytest-runner

%description -n python3-%{modname}
%{summary}.

Python 3 version.
%endif

%package doc
Summary:        Documentation for %{name}
BuildRequires:  python-sphinx

%description doc
%{summary}.

%prep
%autosetup -n %{modname}-%{version}

sed -i -e '/--/d' pytest.ini

%build
%py2_build
%if %{with python3}
%py3_build
%endif
sphinx-build -b html docs html

%install
%py2_install
%if %{with python3}
%py3_install
%endif
rm -f html/.buildinfo

%check
#%{__python2} setup.py test
#%if %{with python3}
#%{__python3} setup.py test
#%endif

%files -n python2-%{modname}
%license LICENSE
%doc README.rst
%{python2_sitelib}/%{modname}*

%if %{with python3}
%files -n python3-%{modname}
%license LICENSE
%doc README.rst
%{python3_sitelib}/%{modname}*
%endif

%files doc
%doc html

%changelog
* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Wed Jan 18 2017 Igor Gnatenko <ignatenko@redhat.com> - 1.0.1-1
- Update to 1.0.1

* Mon Dec 19 2016 Miro Hrončok <mhroncok@redhat.com> - 0.6.1-2
- Rebuild for Python 3.6

* Tue Sep 06 2016 Igor Gnatenko <i.gnatenko.brain@gmail.com> - 0.6.1-1
- Update to 0.6.1

* Tue Jul 19 2016 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5.6-2
- https://fedoraproject.org/wiki/Changes/Automatic_Provides_for_Python_RPM_Packages

* Thu Jun 16 2016 Igor Gnatenko <ignatenko@redhat.com> - 0.5.6-1
- Update to 0.5.6
- Add doc subpkg

* Sun Dec 06 2015 Igor Gnatenko <i.gnatenko.brain@gmail.com> - 0.5.4-1.gitb0de666
- Initial package
