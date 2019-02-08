srpm:
	cd $(outdir)
	dnf -y install rpm-build rpmdevtools
	spectool -A -g $(specfile)
	rpmbuild -bs -D '_sourcedir .' $(specfile)
