%global goipath github.com/mikefarah/yq/v3
%global forgeurl https://github.com/mikefarah/yq
Version:        3.3.2
%global tag     3.3.2

# This is all a workaround for EL7
%if %{?forgemeta:0}%{!?forgemeta:1}
%global repo yq
%global goname golang-github-mikefarah-yq
%global gourl %{forgeurl}
%global archivename %{repo}-%{tag}
%global archiveext tar.gz
%global gosource %{forgeurl}/archive/%{tag}.%{archiveext}#/%{archivename}.%{archiveext}
# https://bugzilla.redhat.com/show_bug.cgi?id=995136#c12
%global _dwz_low_mem_die_limit 0

BuildRequires:  golang

%else
%gometa
%forgemeta
%endif

%global common_description %{expand:
yq is a lightweight and portable command-line YAML processor.
The aim of the project is to be the jq or sed of yaml files.}

%global golicenses    LICENSE
%global godocs        *.md

Name:           %{goname}
Release:        1%{?dist}
Summary:        Process YAML documents from the CLI

License:        MIT
URL:            %{gourl}
Source0:        %{gosource}



%global debug_package %{nil}

%description
%{common_description}

%prep
%autosetup -n %{archivename}

%build
%if %{?gobuild:1}%{!?gobuild:0}
%gobuild -o bin/yq %{goipath}
%else
# CentOS 7 doesn't have the "%gobuild" macro
go build -a -ldflags "-B 0x$(head -c20 /dev/urandom|od -An -tx1|tr -d ' \n') -linkmode=external" -v -x  -o bin/yq   %{goipath}
%endif

# # Build the yq binary - requires internet for dependencies
# # ldflags are needed to generate a BuildID
# go build -o bin/%{name} -a -ldflags "-B 0x$(head -c20 /dev/urandom|od -An -tx1|tr -d ' \n') -linkmode=external" -v -x

%install
install -m 0755 -vd %{buildroot}%{_bindir}
install -m 0755 -vp bin/* %{buildroot}%{_bindir}/

%check
%if %{?gotest:1}%{!?gotest:0}
%gotest
%else
# CentOS 7 doesn't have the "%gotest" macro
go test -compiler gc -ldflags ''
%endif

%files
%license %{golicenses}
%doc %{godocs}
%{_bindir}/*

%changelog
* Mon Jul 6 2020 Derek Ditch <derek@rocknsm.io> 3.3.2-1
- Update to latest version upstream
- Update specfile to golang RPM pkg standards

* Mon Mar 25 2019 Bradford Dabbs <brad@perched.io> 2.3.0-1
 - Initial creation of spec file
