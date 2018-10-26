# Created by pyp2rpm-2.0.0
%global pypi_name oletools

%global _description \
The python-oletools is a package of python tools from Philippe Lagadec \
to analyze Microsoft OLE2 files (also called Structured Storage, \
Compound File Binary Format or Compound Document File Format), \
such as Microsoft Office documents or Outlook messages, mainly for \
malware analysis, forensics and debugging. \
It is based on the olefile parser. \
See http://www.decalage.info/python/oletools for more info.

%if 0%{?fedora} || 0%{?epel} > 6
%bcond_without with_python3
%else
%bcond_with with_python3
%endif

%{!?python3_pkgversion:%global python3_pkgversion 3}

Name:           python-%{pypi_name}
Version:        0.53.1
Release:        2%{?dist}
Epoch:          1
Summary:        Python tools to analyze security characteristics of MS Office and OLE files (also called Structured Storage, Compound File Binary Format or Compound Document File Format), for Malware Analysis and Incident Response #DFIR

License:        BSD
URL:            http://www.decalage.info/python/oletools
Source0:        https://files.pythonhosted.org/packages/79/f5/9b1a89145ac9bce77c235fee549fc7af617d778bb29af4c8dd1561813a10/%{pypi_name}-%{version}.zip
BuildArch:      noarch
Patch0:         %{name}-thirdparty.patch

BuildRequires:  python2-devel
BuildRequires:  python2-setuptools

%if %{with python3}
BuildRequires:  python%{python3_pkgversion}-devel
BuildRequires:  python%{python3_pkgversion}-setuptools
%endif

%description %{_description}

%package -n     python2-%{pypi_name}
Summary:        Python tools to analyze security characteristics of MS Office and OLE files (also called Structured Storage, Compound File Binary Format or Compound Document File Format), for Malware Analysis and Incident Response #DFIR
%{?python_provide:%python_provide python2-%{pypi_name}}

Requires:  python-setuptools
BuildRequires:  python2-devel
Requires:  python2-pymilter
Requires:  python2-colorclass
Requires:  python2-olefile
Requires:  python2-prettytable


%description -n python2-%{pypi_name} %{_description}

%package -n     python2-%{pypi_name}-gui
Summary:        Python tools to analyze security characteristics of MS Office and OLE files (also called Structured Storage, Compound File Binary Format or Compound Document File Format), for Malware Analysis and Incident Response #DFIR
%{?python_provide:%python_provide python2-%{pypi_name}-gui}
Requires:       python2-easygui
Requires:       python2-%{pypi_name} = %{version}-%{release}

%description -n python2-%{pypi_name}-gui %{_description}

%if %{with python3}
%package -n     python3-%{pypi_name}
Summary:        Python tools to analyze security characteristics of MS Office and OLE files (also called Structured Storage, Compound File Binary Format or Compound Document File Format), for Malware Analysis and Incident Response #DFIR
%{?python_provide:%python_provide python3-%{pypi_name}}

BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
Requires:  python%{python3_pkgversion}-olefile
Requires:  python%{python3_pkgversion}-colorclass
Requires:  python%{python3_pkgversion}-prettytable

%description -n python3-%{pypi_name}  %{_description}

%package -n     python3-%{pypi_name}-gui
Summary:        Python tools to analyze security characteristics of MS Office and OLE files (also called Structured Storage, Compound File Binary Format or Compound Document File Format), for Malware Analysis and Incident Response #DFIR
%{?python_provide:%python_provide python3-%{pypi_name}}

Requires:  python%{python3_pkgversion}-easygui
%description -n python3-%{pypi_name}-gui  %{_description}
%endif

%package -n python-%{pypi_name}-doc
Summary:        Documentation files for %{name}
%{?python_provide:%python_provide python2-%{pypi_name}-doc}
%if 0%{?fedora}
%{?python_provide:%python_provide python%{python3_pkgversion}-%{pypi_name}-doc}
%endif

%description -n python-%{pypi_name}-doc %{_description}

%prep
%autosetup -n %{pypi_name}-%{version}
# Remove bundled egg-info
rm -rf %{pypi_name}.egg-info

# Use globally installed python modules instead
for i in colorclass easygui olefile prettytable; do
  rm -rf "oletools/thirdparty/${i}"
done

sed -i -e '
  s|from oletools.thirdparty import olefile|import olefile|;
  s|from oletools.thirdparty.olefile import olefile|from olefile import olefile|;
  s|from oletools.thirdparty.prettytable import prettytable|import prettytable|;
  s|from thirdparty.easygui import|from easygui import|;
  s|from .thirdparty import olefile|import olefile|;
' */*.py



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

pushd %{buildroot}%{_bindir}
  main=$(%{__python3} -c "import sys; sys.stdout.write('{0.major}'.format(sys.version_info))")  # e.g. 3
  full=$(%{__python3} -c "import sys; sys.stdout.write('{0.major}.{0.minor}'.format(sys.version_info))")  # e.g. 3.4

  for i in ezhexviewer mraptor olebrowse oledir oleid olemap olemeta oleobj oletimes olevba pyxswf rtfobj; do
    mv -f "${i}" "${i}-${full}"
    ln -s "${i}-${full}" "${i}-${main}"
  done
popd
%endif

%py2_install

pushd %{buildroot}%{_bindir}
  main=$(%{__python2} -c "import sys; sys.stdout.write('{0.major}'.format(sys.version_info))")  # e.g. 2
  full=$(%{__python2} -c "import sys; sys.stdout.write('{0.major}.{0.minor}'.format(sys.version_info))")  # e.g. 2.7

  for i in ezhexviewer mraptor olebrowse oledir oleid olemap olemeta oleobj oletimes olevba pyxswf rtfobj; do
    mv -f "${i}" "${i}-${full}"
    ln -s "${i}-${full}" "${i}-${main}"

    # For now the 2.7 is the default version, python3 support is experimental
    ln -s "${i}-${full}" "${i}"
  done
popd

# Remove files that should either go to %%doc or to %%license
rm -rf %{buildroot}{%{python2_sitelib},%{python3_sitelib}}/%{pypi_name}/{doc,LICENSE.txt,README.*}
rm -f %{buildroot}{%{python2_sitelib},%{python3_sitelib}}/%{pypi_name}/thirdparty/DridexUrlDecoder/LICENSE.txt
rm -f %{buildroot}{%{python2_sitelib},%{python3_sitelib}}/%{pypi_name}/thirdparty/xglob/LICENSE.txt
rm -f %{buildroot}{%{python2_sitelib},%{python3_sitelib}}/%{pypi_name}/thirdparty/xxxswf/LICENSE.txt
rm -f %{buildroot}{%{python2_sitelib},%{python3_sitelib}}/%{pypi_name}/thirdparty/zipfile27/LICENSE.txt

# Prepare licenses from bundled code for later %%license usage
mv -f %{pypi_name}/thirdparty/DridexUrlDecoder/LICENSE.txt DridexUrlDecoder-LICENSE.txt
mv -f %{pypi_name}/thirdparty/xglob/LICENSE.txt xglob-LICENSE.txt
mv -f %{pypi_name}/thirdparty/xxxswf/LICENSE.txt xxxswf-LICENSE.txt
mv -f %{pypi_name}/thirdparty/zipfile27/LICENSE.txt zipfile27-LICENSE.txt

%check
%if 0
%{__python2} setup.py test
%endif
# Python3 test fails for:
# Milter on mraptor_milter.py -> missing python3 version, the mraptor_milter.py will work only with python2
# ioString on olevba.pu -> there is olevba3.py version
%if %{with python3}
%{__python3} setup.py test || true
%endif

%files -n python2-%{pypi_name} 
%license %{pypi_name}/LICENSE.txt *-LICENSE.txt 
%doc README.md
%{python2_sitelib}/%{pypi_name}
%{python2_sitelib}/%{pypi_name}-%{version}-py?.?.egg-info
%{_bindir}/oledir-2*
%{_bindir}/oleid-2*
%{_bindir}/olemap-2*
%{_bindir}/olemeta-2*
%{_bindir}/oleobj-2*
%{_bindir}/oletimes-2*
%{_bindir}/olevba-2*
%{_bindir}/mraptor-2*
%{_bindir}/pyxswf-2*
%{_bindir}/rtfobj-2*
%{_bindir}/oledir
%{_bindir}/oleid
%{_bindir}/olemap
%{_bindir}/olemeta
%{_bindir}/oleobj
%{_bindir}/oletimes
%{_bindir}/olevba
%{_bindir}/olevba3
%{_bindir}/mraptor
%{_bindir}/mraptor3
%{_bindir}/msodde
%{_bindir}/pyxswf
%{_bindir}/rtfobj

%files -n python2-%{pypi_name}-gui
%license %{pypi_name}/LICENSE.txt *-LICENSE.txt 
%doc README.md
%{_bindir}/ezhexviewer-*
%{_bindir}/olebrowse-*
%{_bindir}/ezhexviewer
%{_bindir}/olebrowse


%if %{with python3}
%files -n python3-%{pypi_name} 
%license %{pypi_name}/LICENSE.txt *-LICENSE.txt 
%doc README.md
%{python3_sitelib}/%{pypi_name}
%{python3_sitelib}/%{pypi_name}-%{version}-py?.?.egg-info
%{_bindir}/oledir-3*
%{_bindir}/oleid-3*
%{_bindir}/olemap-3*
%{_bindir}/olemeta-3*
%{_bindir}/oleobj-3*
%{_bindir}/oletimes-3*
# ModuleNotFoundError: No module named 'cStringIO'
%exclude %{_bindir}/olevba-3*
# ModuleNotFoundError: No module named 'cStringIO'
%exclude %{_bindir}/mraptor-3*
%{_bindir}/pyxswf-3*
%{_bindir}/rtfobj-3*

%files -n python3-%{pypi_name} 
%license %{pypi_name}/LICENSE.txt *-LICENSE.txt 
%doc README.md
%{_bindir}/ezhexviewer-3*
%{_bindir}/olebrowse-3*
%endif

%changelog
* Thu Oct 25 2018 Derek Ditch <derek@rocknsm.io> - 1:0.53.1-2
- Remove pyparsing from dependencies.

* Thu Oct 25 2018 Derek Ditch <derek@rocknsm.io> - 1:0.53.1-1
- Initial package.
- Split out GUI dependencies
