YUM := $(shell command -v dnf 2> /dev/null)
ifndef YUM
YUM := $(shell command -v yum 2> /dev/null)
endif

srpm:
	cd $(outdir); \
	cp $(spec) ./ ; \
	$(YUM) -y install rpm-build rpmdevtools; \
	spectool -A -g $(spec); \
	chown root:root *; \
	rpmbuild -bs -D '_sourcedir .' -D "_srcrpmdir $(outdir)" *.spec
