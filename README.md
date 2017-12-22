# RPM sources

These are the spec files and related patches, etc used for RockNSM dependencies that are not included in the upstream OS or EPEL. The only packages not here are the RockNSM-specific packages. Those spec files are integrated into their respective repositories on GitHub.

These packages are currently built over at [RockNSM Copr](https://copr.fedorainfracloud.org/coprs/g/rocknsm/rocknsm-2.1). Here's the steps I use to produce the source RPM (SRPM):

## Building the SRPMs

Go into each directory and run:

```
spectool -a -g <pkgname>.spec
mock -r epel-7-x86_64 --buildsrpm --spec=<pkgname>.spec --sources=. --resultdir=SRPMS/
```

The first command will download all the sources needed for the package. The second will actually build the SRPM and place the package into the `SRPMS/` directory. From there you can upload to a service like Copr, build with `mock`, or use the classical way of building RPMs with `rpmbuild`.
