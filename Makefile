#!/usr/bin/env make -f

# Python Repo Template
# ..................................
# Copyright (c) 2017, Kendrick Walls
# ..................................
# Licensed under MIT (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# ..........................................
# http://www.github.com/reactive-firewall/python-repo/LICENSE.md
# ..........................................
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


ifeq "$(ECHO)" ""
	ECHO=echo
endif

ifeq "$(LINK)" ""
	LINK=ln -sf
endif

ifeq "$(MAKE)" ""
	MAKE=make
endif

ifeq "$(WAIT)" ""
	WAIT=wait
endif

ifeq "$(INSTALL)" ""
	INSTALL=install
	ifeq "$(INST_OWN)" ""
		INST_OWN=-o root -g staff
	endif
	ifeq "$(INST_OPTS)" ""
		INST_OPTS=-m 755
	endif
endif

ifeq "$(LOG)" ""
	LOG=no
endif

ifeq "$(LOG)" "no"
	QUIET=@
endif

ifeq "$(DO_FAIL)" ""
	DO_FAIL=$(ECHO) "ok"
endif

PHONY: must_be_root cleanup

build:
	$(QUIET)$(ECHO) "No need to build. Try make -f Makefile install"

init:
	$(QUIET)$(ECHO) "$@: Done."

install: must_be_root
	$(QUIET)python3 -m pip install "git+https://github.com/reactive-firewall/pythonrepo.git#egg=pythonrepo"
	$(QUITE)$(WAIT)
	$(QUIET)$(ECHO) "$@: Done."

uninstall:
	$(QUITE)$(QUIET)python3 -m pip uninstall pythonrepo || true
	$(QUITE)$(WAIT)
	$(QUIET)$(ECHO) "$@: Done."

purge: clean uninstall
	$(QUIET)python3 -m pip uninstall pythonrepo && python -m pip uninstall pythonrepo || true
	$(QUIET)$(ECHO) "$@: Done."

test: cleanup
	$(QUIET)coverage run -p --source=pythonrepo -m unittest discover --verbose -s ./tests -t ./ || python3 -m unittest discover --verbose -s ./tests -t ./ || python -m unittest discover --verbose -s ./tests -t ./ || DO_FAIL=exit 2 ;
	$(QUIET)coverage combine 2>/dev/null || true
	$(QUIET)coverage report --include=pythonrepo* 2>/dev/null || true
	$(QUIET)$(DO_FAIL);
	$(QUIET)$(ECHO) "$@: Done."

test-tox: cleanup
	$(QUIET)tox -v --
	$(QUIET)$(ECHO) "$@: Done."

test-style: cleanup
	$(QUIET)flake8 --ignore=W191,W391 --max-line-length=100 --verbose --count
	$(QUIET)$(ECHO) "$@: Done."

cleanup:
	$(QUIET)rm -f tests/*.pyc 2>/dev/null || true
	$(QUIET)rm -f tests/*~ 2>/dev/null || true
	$(QUIET)rm -Rf tests/__pycache__ 2>/dev/null || true
	$(QUIET)rm -f pythonrepo/*.pyc 2>/dev/null || true
	$(QUIET)rm -Rf pythonrepo/__pycache__ 2>/dev/null || true
	$(QUIET)rm -Rf pythonrepo/*/__pycache__ 2>/dev/null || true
	$(QUIET)rm -f pythonrepo/*~ 2>/dev/null || true
	$(QUIET)rm -f *.pyc 2>/dev/null || true
	$(QUIET)rm -f pythonrepo/*/*.pyc 2>/dev/null || true
	$(QUIET)rm -f pythonrepo/*/*~ 2>/dev/null || true
	$(QUIET)rm -f *.DS_Store 2>/dev/null || true
	$(QUIET)rm -f pythonrepo/*.DS_Store 2>/dev/null || true
	$(QUIET)rm -f pythonrepo/*/*.DS_Store 2>/dev/null || true
	$(QUIET)rm -f pythonrepo.egg-info/* 2>/dev/null || true
	$(QUIET)rmdir pythonrepo.egg-info 2>/dev/null || true
	$(QUIET)rm -f ./*/*~ 2>/dev/null || true
	$(QUIET)rm -f ./*~ 2>/dev/null || true
	$(QUIET)coverage erase 2>/dev/null || true
	$(QUIET)rm -f ./.coverage 2>/dev/null || true
	$(QUIET)rm -f ./coverage*.xml 2>/dev/null || true
	$(QUIET)rm -f ./sitecustomize.py 2>/dev/null || true
	$(QUIET)rm -f ./.*~ 2>/dev/null || true
	$(QUIET)rm -Rf ./.tox/ 2>/dev/null || true

clean: cleanup
	$(QUIET)$(MAKE) -s -C ./docs/ -f Makefile clean 2>/dev/null || true
	$(QUIET)$(ECHO) "$@: Done."

must_be_root:
	$(QUIET)runner=`whoami` ; \
	if test $$runner != "root" ; then echo "You are not root." ; exit 1 ; fi

%:
	$(QUIET)$(ECHO) "No Rule Found For $@" ; $(WAIT) ;

