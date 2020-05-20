mkfile_path := $(abspath $(lastword $(MAKEFILE_LIST)))
top_dir := $(notdir $(patsubst %/,%,$(dir $(mkfile_path))))
SRPM := $(shell rpmspec --query --srpm --queryformat '%{name}-%{version}-%{release}\n' $(spec)).src.rpm
SOURCES := $(shell spectool --list $(spec)| sed 's|^.*[ \/]||g')
outdir:= output

sources: $(SOURCES)

$(SOURCES): $(spec)
	mkdir -p $(outdir)
	spectool -A -g -C $(outdir) $(spec)
	for item in $(shell spectool -l $(spec) | awk '$$0 !~ /http/ { print $$2}'); do \
            cp $(shell dirname $(spec))/$${item} $(outdir); \
	done

$(outdir)/$(SRPM): $(SOURCES)
	mock --buildsrpm --sources=$(outdir) --spec $(spec) --resultdir=$(outdir)

srpm: $(outdir)/$(SRPM)

rpm: $(outdir)/$(SRPM)
	mock -r rock-8-x86_64.cfg --resultdir=$(outdir) $(outdir)/$(SRPM) --no-cleanup-after
	createrepo_c --update $(outdir)

copr: $(outdir)/$(SRPM)
	copr-cli build -r epel-7-x86_64 @rocknsm/testing $(outdir)/$(SRPM)
