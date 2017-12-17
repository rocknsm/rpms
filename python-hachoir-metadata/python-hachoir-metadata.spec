# Created by pyp2rpm-3.2.2
%global pypi_name hachoir-metadata

Name:           python-%{pypi_name}
Version:        1.3.3
Release:        1%{?dist}
Summary:        Program to extract metadata using Hachoir library

License:        GNU GPL v2
URL:            http://bitbucket.org/haypo/hachoir/wiki/hachoir-metadata
Source0:        https://files.pythonhosted.org/packages/source/h/%{pypi_name}/%{pypi_name}-%{version}.tar.gz
BuildArch:      noarch
 
BuildRequires:  python2-devel
BuildRequires:  python-setuptools

%description
hachoirmetadata extracts metadata from multimedia files: music, picture, video,
but also archives. It supports most common file formats: * Archives: bzip2,
gzip, zip, tar * Audio: MPEG audio ("MP3"), WAV, Sun/NeXT audio, Ogg/Vorbis
(OGG), MIDI, AIFF, AIFC, Real audio (RA) * Image: BMP, CUR, EMF, ICO, GIF,
JPEG, PCX, PNG, TGA, TIFF, WMF, XCF * Misc: Torrent * Program: EXE * Video: ASF
format...

%package -n     python2-%{pypi_name}
Summary:        %{summary}
%{?python_provide:%python_provide python2-%{pypi_name}}

%description -n python2-%{pypi_name}
hachoirmetadata extracts metadata from multimedia files: music, picture, video,
but also archives. It supports most common file formats: * Archives: bzip2,
gzip, zip, tar * Audio: MPEG audio ("MP3"), WAV, Sun/NeXT audio, Ogg/Vorbis
(OGG), MIDI, AIFF, AIFC, Real audio (RA) * Image: BMP, CUR, EMF, ICO, GIF,
JPEG, PCX, PNG, TGA, TIFF, WMF, XCF * Misc: Torrent * Program: EXE * Video: ASF
format...


%prep
%autosetup -n %{pypi_name}-%{version}
# Remove bundled egg-info
rm -rf %{pypi_name}.egg-info

%build
%py2_build

%install
%py2_install
cp %{buildroot}/%{_bindir}/hachoir-metadata %{buildroot}/%{_bindir}/hachoir-metadata-%{python2_version}
ln -s %{_bindir}/hachoir-metadata-%{python2_version} %{buildroot}/%{_bindir}/hachoir-metadata-2
cp %{buildroot}/%{_bindir}/hachoir-metadata-qt %{buildroot}/%{_bindir}/hachoir-metadata-qt-%{python2_version}
ln -s %{_bindir}/hachoir-metadata-qt-%{python2_version} %{buildroot}/%{_bindir}/hachoir-metadata-qt-2
cp %{buildroot}/%{_bindir}/hachoir-metadata-gtk %{buildroot}/%{_bindir}/hachoir-metadata-gtk-%{python2_version}
ln -s %{_bindir}/hachoir-metadata-gtk-%{python2_version} %{buildroot}/%{_bindir}/hachoir-metadata-gtk-2


%files -n python2-%{pypi_name}
%doc 
%{_bindir}/hachoir-metadata
%{_bindir}/hachoir-metadata-2
%{_bindir}/hachoir-metadata-%{python2_version}
%{_bindir}/hachoir-metadata-qt
%{_bindir}/hachoir-metadata-qt-2
%{_bindir}/hachoir-metadata-qt-%{python2_version}
%{_bindir}/hachoir-metadata-gtk
%{_bindir}/hachoir-metadata-gtk-2
%{_bindir}/hachoir-metadata-gtk-%{python2_version}
%{python2_sitelib}/hachoir_metadata
%{python2_sitelib}/hachoir_metadata-%{version}-py?.?.egg-info

%changelog
* Thu Nov 30 2017 Derek Ditch <derek@rocknsm.io> - 1.3.3-1
- Initial package.