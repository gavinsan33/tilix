# Used by Fedora COPR ("make srpm" SCM method) to build a source RPM from this checkout
top := $(abspath $(dir $(lastword $(MAKEFILE_LIST)))/..)
outdir ?= $(top)
spec ?= $(top)/tilix.spec
git = git -c safe.directory=$(top) -C $(top)

srpm:
	command -v git >/dev/null || dnf -y install git-core
	$(git) archive --prefix=tilix/ -o $(outdir)/tilix.tar.gz HEAD
	rpmbuild -bs $(spec) \
		--define "_sourcedir $(outdir)" --define "_srcrpmdir $(outdir)" \
		--define "snapshot $$($(git) rev-list --count HEAD).git$$($(git) rev-parse --short HEAD)"
