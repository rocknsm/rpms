# Copyright 2017-2018 RockNSM
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

Name:           rock-release
Version:        2.3
Release:        2
Summary:        RockNSM repository configuration

Group:          System Environment/Base
License:        GPLv2

# This is a RockNSM maintained package which is specific to
# our distribution.  Thus the source is only available from
# within this srpm.
URL:            http://rocknsm.io
Source0:        http://rocknsm.io/RPM-GPG-KEY-RockNSM-2
Source1:        LICENSE
Source2:        rocknsm.repo
Source3:        rocknsm-testing.repo
Source4:        https://packagecloud.io/rocknsm/2_3/gpgkey#/RPM-GPG-KEY-RockNSM-pkgcloud-2_3
Source5:	https://copr-be.cloud.fedoraproject.org/results/@rocknsm/testing/pubkey.gpg#/RPM-GPG-KEY-RockNSM-Testing

BuildArch:     noarch
Requires:      redhat-release >= 7
# epel-release is only for enterprise linux, not fedora
Conflicts:     fedora-release

%description
This package contains the Response Operations Collection Kit NSM (RockNSM)
repository GPG key as well as configuration for yum.

%prep
%setup -q  -c -T
install -pm 644 %{SOURCE0} .
install -pm 644 %{SOURCE1} .
install -pm 644 %{SOURCE4} .
install -pm 644 %{SOURCE5} .

%build

%install
rm -rf $RPM_BUILD_ROOT

#GPG Key
install -Dpm 644 %{SOURCE0} \
    $RPM_BUILD_ROOT%{_sysconfdir}/pki/rpm-gpg/RPM-GPG-KEY-RockNSM-2
install -Dpm 644 %{SOURCE4} \
    $RPM_BUILD_ROOT%{_sysconfdir}/pki/rpm-gpg/RPM-GPG-KEY-RockNSM-pkgcloud-2_3
install -Dpm 644 %{SOURCE5} \
    $RPM_BUILD_ROOT%{_sysconfdir}/pki/rpm-gpg/RPM-GPG-KEY-RockNSM-Testing


# yum
install -dm 755 $RPM_BUILD_ROOT%{_sysconfdir}/yum.repos.d
install -pm 644 %{SOURCE2} %{SOURCE3}  \
    $RPM_BUILD_ROOT%{_sysconfdir}/yum.repos.d

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%doc LICENSE
%config(noreplace) /etc/yum.repos.d/*
/etc/pki/rpm-gpg/*

%changelog
* Sun Feb 17 2019 Jeff Geiger <jeff@rocknsm.io> - 2.3-2
- Updated packagecloud GPG key download

* Fri Feb 15 2019 Derek Ditch <derek@rocknsm.io> - 2.3-1
- Updated package to 2.3-1

* Mon Oct 29 2018 Derek Ditch <derek@rocknsm.io> - 2.2-3
- Fixed typo in GPG keyname
- Disable repo_gpgcheck, not supported by copr

* Fri Oct 26 2018 Derek Ditch <derek@rocknsm.io> - 2.2-1
- Bumped version to 2.2

* Sun Mar 4 2018 Derek Ditch <derek@rocknsm.io> - 2.1-2
- Added GPG pub key for testing repo

* Fri Feb 23 2018 Derek Ditch <derek@rocknsm.io> - 2.1-1
- Initial release. Contains stable and testing repos.
