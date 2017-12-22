# Created by pyp2rpm-3.2.2
%global pypi_name asn1crypto

%if 0%{?fedora} || 0%{?epel} > 6
%bcond_without with_python3
%else
%bcond_with with_python3
%endif

%{!?python3_pkgversion:%global python3_pkgversion 3}

Name:           python-%{pypi_name}
Version:        0.23.0
Release:        2%{?dist}
Summary:        Fast Python ASN.1 parser and serializer

License:        MIT
URL:            https://github.com/wbond/asn1crypto
Source0:        https://files.pythonhosted.org/packages/source/a/%{pypi_name}/%{pypi_name}-%{version}.tar.gz
BuildArch:      noarch

BuildRequires:  python2-devel
BuildRequires:  python2-setuptools

%if %{with python3}
BuildRequires:  python%{python3_pkgversion}-devel
BuildRequires:  python%{python3_pkgversion}-setuptools
%endif

%description
Fast ASN.1 parser and serializer with definitions for private keys,
public keys, certificates, CRL, OCSP, CMS, PKCS#3, PKCS#7, PKCS#8,
PKCS#12, PKCS#5, X.509 and TSP.

%package -n     python2-%{pypi_name}
Summary:        %{summary}
%{?python_provide:%python_provide python2-%{pypi_name}}

%description -n python2-%{pypi_name}
Fast ASN.1 parser and serializer with definitions for private keys,
public keys, certificates, CRL, OCSP, CMS, PKCS#3, PKCS#7, PKCS#8,
PKCS#12, PKCS#5, X.509 and TSP.

%if %{with python3}
%package -n     python%{python3_pkgversion}-%{pypi_name}
Summary:        %{summary}
%{?python_provide:%python_provide python%{python3_pkgversion}-%{pypi_name}}

%description -n python%{python3_pkgversion}-%{pypi_name}
Fast ASN.1 parser and serializer with definitions for private keys,
public keys, certificates, CRL, OCSP, CMS, PKCS#3, PKCS#7, PKCS#8,
PKCS#12, PKCS#5, X.509 and TSP.
%endif

%prep
%autosetup -n %{pypi_name}-%{version}
# Remove bundled egg-info
rm -rf %{pypi_name}.egg-info

%build
%py2_build
%if %{with python3}
%py3_build
%endif

%install
# Must do the subpackages' install first because the scripts in /usr/bin are
# overwritten with every setup.py install.
%if %{with python3}
%py3_install
%endif

%py2_install


%check
# asn1crypto source distribution doesn't come with tests
# {__python2} setup.py test
%if %{with python3}
# {__python3} setup.py test
%endif

%files -n python2-%{pypi_name}
%doc
%{python2_sitelib}/%{pypi_name}
%{python2_sitelib}/%{pypi_name}-%{version}-py?.?.egg-info

%if %{with python3}
%files -n python%{python3_pkgversion}-%{pypi_name}
%doc
%{python3_sitelib}/%{pypi_name}
%{python3_sitelib}/%{pypi_name}-%{version}-py?.?.egg-info
%endif

%changelog
* Fri Dec 22 2017 Derek Ditch <derek@rocknsm.io> - 0.23-2
- Added spec guards to package for EL7

* Thu Oct 12 2017 Christian Heimes <cheimes@redhat.com> - 0.23-1
- New upstream release 0.23.0

* Fri Aug 04 2017 Christian Heimes <cheimes@redhat.com> - 0.22.0-5
- Use python2-setuptools, add with_python3

* Thu Aug 03 2017 Christian Heimes <cheimes@redhat.com> - 0.22.0-4
- Modernize spec

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.22.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Tue Jun 27 2017 Christian Heimes <cheimes@redhat.com> - 0.22.0-2
- Address rpmlint issues

* Tue Jun 27 2017 Christian Heimes <cheimes@redhat.com> - 0.22.0-1
- Initial package.
