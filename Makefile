
VERSION = 1.0.0
NAME    = cassandra-tools-wmf

PREFIX   ?= /usr
BINDIR   ?= $(DESTDIR)/$(PREFIX)/bin
SHAREDIR ?= $(DESTDIR)/$(PREFIX)/share/$(NAME)

all:

install:
	install -m 755 -d $(BINDIR)
	install -m 755 -d $(SHAREDIR)
	install -m 755 c-ls $(BINDIR)
	install -m 755 c-foreach-nt $(BINDIR)
	install -m 755 c-cqlsh $(BINDIR)
	install -m 755 c-any-nt $(BINDIR)
	install -m 755 streams $(BINDIR)/cassandra-streams
	install -m 755 uyaml $(BINDIR)
	install -m 644 functions $(SHAREDIR)

orig.tar.gz:
	git archive --format=tar.gz --prefix=$(NAME)-$(VERSION)/ \
	    -o ../$(NAME)_$(VERSION).orig.tar.gz HEAD

lint:
	# Run pylint; Fail if exit status means 'error' or 'fatal'
	pylint --rcfile=.pylintrc cassandra; \
	    echo "pylint returned exit code $$?"; \
	    if [ "$$(($$? & 1))" != 0 ] || [ "$$(($$? & 2))" != 0 ]; then \
	        false; \
	    else \
	        true; \
	    fi
