srpm:
	cd $(outdir)
	dnf -y install rpm-build rpmdevtools
	spectool -A -g $(spec)
	rpmbuild -bs -D '_sourcedir .' -D "_srcrpmdir $(outdir)" $(spec)
