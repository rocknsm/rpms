# Created by pyp2rpm-3.2.2
%global distname macholibre
%global commit0 95aa61a5bdd224ba2ac973e2aa839d736f522302
%global shortcommit0 %(c=%{commit0}; echo ${c:0:7})
%global commitdate 20171114

Name:           python-%{distname}
Version:        0.2
Release:        1.%{commitdate}git%{shortcommit0}%{?dist}
Summary:        Mach-O & Universal Binary Parser

License:        ASL 2.0
URL:            https://github.com/aaronst/macholibre
Source0:        https://github.com/aaronst/%{distname}/archive/%{commit0}.tar.gz#/%{name}-%{shortcommit0}.tar.gz
BuildArch:      noarch

BuildRequires:  python2-devel
BuildRequires:  python-setuptools

%description
macholibre is a Mach-O and Universal binary parser. It extracts information such
as architectures, load commands, dynamic libraries, symbols, function imports,
and tons more. Then it packs all of that information into JSON for ease of
analysis and integration.

%package -n     python2-%{distname}
Summary:        %{summary}
%{?python_provide:%python_provide python2-%{distname}}
Requires:       python2-asn1crypto

%description -n python2-%{distname}
macholibre is a Mach-O and Universal binary parser. It extracts information such
as architectures, load commands, dynamic libraries, symbols, function imports,
and tons more. Then it packs all of that information into JSON for ease of
analysis and integration.


%prep
%setup -n %{distname}-%{commit0}
# Remove bundled egg-info
rm -rf %{distname}.egg-info

%build
%py2_build

%install
%py2_install
cp %{buildroot}/%{_bindir}/macholibre %{buildroot}/%{_bindir}/macholibre-%{python2_version}
ln -s %{_bindir}/macholibre-%{python2_version} %{buildroot}/%{_bindir}/macholibre-2


%files -n python2-%{distname}
%doc
%{_bindir}/macholibre
%{_bindir}/macholibre-%{python2_version}
%{_bindir}/macholibre-2

%{python2_sitelib}/macholibre
%{python2_sitelib}/macholibre-%{version}-py?.?.egg-info

%changelog
* Tue Dec 12 2017 Derek Ditch <derek@rocknsm.io> - 0.2-1.20171114git95aa61a
- Initial package.
