srpm:
	cd $(outdir)
	dnf -y install spectool rpmbuild
	spectool -a -g $(specfile)
	rpmbuild -bs -D '_sourcedir .' $(specfile)
