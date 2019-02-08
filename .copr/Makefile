srpm:
	cd $(outdir)
	dnf -y install rpm-build rpmdevtools
	spectool -a -g $(specfile)
	rpmbuild -bs -D '_sourcedir .' $(specfile)
