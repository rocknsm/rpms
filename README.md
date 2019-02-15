# RPM sources

These are the spec files and related patches, etc used for RockNSM dependencies that are not included in the upstream OS or EPEL. The only packages not here are the RockNSM-specific packages. Those spec files are integrated into their respective repositories on GitHub.

These packages are currently built over at [RockNSM Copr](https://copr.fedorainfracloud.org/coprs/g/rocknsm/rocknsm-2.1). Here's the steps I use to produce the source RPM (SRPM):

## Building the SRPMs

The Makefile will make this easier. It's not perfect, but do something like:

~~~
make rpm spec=suricata/suricata.spec
~~~

This will download all the sources, copy them to `output/` and build the SRPM. It will then create the RPM. Both of these are done using `mock`, so you need to ensure you have that setup first.

There's also a shortcut for submitting to `copr` build service. You need to have `copr-cli` installed and configured with your auth token. Then just run 

~~~
make copr spec=suricata/suricata.spec
~~~

This will build the SRPM locally with `mock` as before, but it will not locally build the RPM. It will instead upload it to `copr` repo for @rocknsm/testing.
