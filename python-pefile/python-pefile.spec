%global srcname pefile

%global common_desc pefile is a multi-platform Python module to read and work with Portable\
Executable (aka PE) files. Most of the information in the PE Header is \
accessible, as well as all the sections, section's information and data.\
pefile requires some basic understanding of the layout of a PE file. Armed \
with it it's possible to explore nearly every single feature of the file.\
Some of the tasks that pefile makes possible are:\
* Modifying and writing back to the PE image\
* Header Inspection\
* Sections analysis\
* Retrieving data\
* Warnings for suspicious and malformed values\
* Packer detection with PEiD’s signatures\
* PEiD signature generation\

%if 0%{?fedora} || 0%{?epel} > 6
%bcond_without with_python3
%else
%bcond_with with_python3
%endif

Name:           python-%{srcname}
Version:        2017.11.5
Release:        1%{?dist}
Summary:        Python module for working with Portable Executable files
License:        MIT
URL:            https://github.com/erocarrera/pefile

Source0:        https://github.com/erocarrera/pefile/archive/v%{version}/pefile-%{version}.tar.gz 
BuildArch:      noarch

BuildRequires:  python2-devel
BuildRequires:  python2-setuptools
%if %{with python3}
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
%endif

# For the patch
# BuildRequires: git-core 

%description
%{common_desc}

%package -n python2-%{srcname}
Summary:        %{summary}
%{?python_provide:%python_provide python2-%{srcname}}
Requires:   python2-future

%description -n python2-%{srcname}
%{common_desc}

%if %{with python3}
%package -n python3-%{srcname}
Summary:        %{summary}
%{?python_provide:%python_provide python3-%{srcname}}
Requires:   python3-future

%description -n python3-%{srcname}
%{common_desc}
%endif

%prep
%autosetup -n %{srcname}-%{version}
sed -i -e '/^#!\//, 1d' pefile.py

%build
%py2_build
%if %{with python3}
%py3_build
%endif

%install
%py2_install
%if %{with python3}
%py3_install
%endif

%check
%{__python2} setup.py test
%if %{with python3}
%{__python3} setup.py test
%endif

%files -n python2-%{srcname}
%license LICENSE
%doc README*
%{python2_sitelib}/*

%if %{with python3}
%files -n python3-%{srcname}
%license LICENSE
%doc README*
%{python3_sitelib}/*
%endif

%changelog
* Wed Nov 08 2017 Athmane Madjoudj <athmane@fedoraproject.org> - 2017.11.5-1
- Update to 2017.11.5 (rhbz #1509751)

* Sat Aug 05 2017 Athmane Madjoudj <athmane@fedoraproject.org> - 2017.8.1-1
- Update to 2017.8.1

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2017.5.26-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Tue Jul 25 2017 Athmane Madjoudj <athmane@fedoraproject.org> - 2017.5.26-2
- Fix requirement (rhbz #1474447)

* Sat May 27 2017 Athmane Madjoudj <athmane@fedoraproject.org> - 2017.5.26-1
- Update to 2017.5.26
- Remove upstreamed patch

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2016.3.28-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Mon Dec 19 2016 Miro Hrončok <mhroncok@redhat.com> - 2016.3.28-2
- Rebuild for Python 3.6

* Tue Nov 01 2016 Athmane Madjoudj <athmane@fedoraproject.org> - 2016.3.28-1
- Update to 2016.3.28
- Revamp the specfile
- Add patch to fix the build

* Tue Jul 19 2016 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.10_139-5
- https://fedoraproject.org/wiki/Changes/Automatic_Provides_for_Python_RPM_Packages

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.10_139-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.10_139-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.10_139-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Tue Jan 07 2014 Christopher Meng <rpm@cicku.me> - 1.2.10_139-1
- Update to 1.2.10_139

* Thu Aug 08 2013 Christopher Meng <rpm@cicku.me> - 1.2.10_123-1
- Update to 1.2.10_123

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.10_63-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.10_63-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.10_63-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.10_63-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.10_63-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Jul 22 2010 David Malcolm <dmalcolm@redhat.com> - 1.2.10_63-3
- Rebuilt for https://fedoraproject.org/wiki/Features/Python_2.7/MassRebuild

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.10_63-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Fri May  8 2009 David Malcolm <dmalcolm@redhat.com> - 1.2.10_63-1
- initial packaging

