# Builds a source RPM from this checkout (used by .github/workflows/rpm-repo.yml)
top := $(abspath $(dir $(lastword $(MAKEFILE_LIST)))/..)
outdir ?= $(top)
spec ?= $(top)/tilix.spec
git = git -c safe.directory=$(top) -C $(top)

srpm:
	command -v git >/dev/null || dnf -y install git-core
	$(git) archive --prefix=tilix/ -o $(outdir)/tilix.tar.gz HEAD
	# Bake the snapshot version into the spec so rebuilding the SRPM keeps it
	{ echo "%global snapshot $$($(git) rev-list --count HEAD).git$$($(git) rev-parse --short HEAD)"; cat $(spec); } > $(outdir)/tilix.spec
	rpmbuild -bs $(outdir)/tilix.spec --define "_sourcedir $(outdir)" --define "_srcrpmdir $(outdir)"
