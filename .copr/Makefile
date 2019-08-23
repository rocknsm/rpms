YUM := $(shell command -v dnf 2> /dev/null)
ifndef YUM
YUM := $(shell command -v yum 2> /dev/null)
endif

srpm:
	$(YUM) -y install rpm-build rpmdevtools; \
	spectool -A -g $(spec) -C $(shell dirname $(spec)); \
	cd $(shell dirname $(spec)); \
	chown root:root *; \
	rpmbuild -bs -D '_sourcedir .' -D "_srcrpmdir $(outdir)" *.spec
