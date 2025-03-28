#!/usr/bin/env make -f

# Python Repo Template
# ..................................
# Copyright (c) 2017-2024, Kendrick Walls
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


ifeq "$(LC_CTYPE)" ""
	LC_CTYPE="en_US.UTF-8"
endif

ifndef SHELL
	SHELL:=command -pv bash
endif

ifeq "$(ERROR_LOG_PATH)" ""
	ERROR_LOG_PATH="/dev/null"
endif

ifeq "$(COMMAND)" ""
	COMMAND_CMD=$(shell command -v xcrun || command -v command || command which which || command -v which)
	COMMAND_TOOL=$(notdir $(COMMAND_CMD))
	ifeq "$(COMMAND_TOOL)" "xcrun"
		COMMAND_ARGS= --find
	endif
	ifeq "$(COMMAND_TOOL)" "command"
		COMMAND_ARGS= -v
	endif
	ifeq "$(COMMAND_CMD)" ""
		COMMAND_CMD="command"
	endif
	ifdef COMMAND_ARGS
		COMMAND := $(COMMAND_CMD) $(COMMAND_ARGS)
	else
		COMMAND := $(COMMAND_CMD)
	endif
endif

ifeq "$(MAKE)" ""
	#  just no cmake please
	MAKEFLAGS=$(MAKEFLAGS) -s
	MAKE!=`$(COMMAND) make 2>$(ERROR_LOG_PATH) || $(COMMAND) gnumake 2>$(ERROR_LOG_PATH)`
endif

ifeq "$(ECHO)" ""
	ECHO=printf "%s\n"
endif

ifdef ACTION
	SET_FILE_ATTR=$(shell $(COMMAND) xattr)
endif

ifdef SET_FILE_ATTR
	CREATEDBYBUILDSYSTEM=-w com.apple.xcode.CreatedByBuildSystem true
	BSMARK=$(SET_FILE_ATTR) $(CREATEDBYBUILDSYSTEM)
else
	BSMARK_CMD=$(shell $(COMMAND) touch)
	BSMARK=$(BSMARK_CMD) -a
endif

ifeq "$(LINK)" ""
	LINK_CMD=$(shell $(COMMAND) ln)
	LINK=$(LINK_CMD) -sf
endif

# Python command configuration
ifeq "$(PYTHON)" ""
	# Try to find python3, fallback to python
	PY_CMD=$(shell $(COMMAND) python3)
	ifneq "$(PY_CMD)" ""
		# Only use -B arg with python3
		PY_ARGS=-B
	else
		PY_CMD=$(shell $(COMMAND) python)
	endif
	# Set PYTHON only if not already set
	PYTHON := $(PY_CMD) $(PY_ARGS)
endif

# Coverage configuration
ifeq "$(COVERAGE)" ""
	# If PYTHON is set (either by us or externally), try module approach first
	ifneq "$(PYTHON)" ""
		COVERAGE=$(PYTHON) -m coverage
	endif
	# If COVERAGE is still not set, fall back to direct command
	ifeq "$(COVERAGE)" ""
		COVERAGE=$(shell $(COMMAND) coverage)
	endif
	# Only set COV_CORE_* variables when COVERAGE is configured
	ifneq "$(COVERAGE)" ""
		#COV_CORE_SOURCE = $(dir $(abspath $(lastword $(MAKEFILE_LIST))))/
		COV_CORE_CONFIG = $(dir $(abspath $(lastword $(MAKEFILE_LIST))))/.coveragerc
		COV_CORE_DATAFILE = .coverage
	endif
endif

ifndef PIP_COMMON_FLAGS
	# Define common pip install flags
	PIP_COMMON_FLAGS := --use-pep517 --exists-action s --upgrade --upgrade-strategy eager
endif

# Define environment-specific flags
ifeq ($(shell uname -s), Darwin)
	PIP_ENV_FLAGS := --break-system-packages
	FETCH_CC_INCLUDE_PATH := includes/fetch-test-reporter/tools-fetch-test-reporter.make
else ifeq ($(shell uname -s), Linux)
	FETCH_CC_INCLUDE_PATH := includes/fetch-test-reporter/tools-fetch-test-reporter.make
else
	FETCH_CC_INCLUDE_PATH := includes\fetch-test-reporter\tools-fetch-test-reporter.make
	PIP_ENV_FLAGS :=
endif

ifeq "$(WAIT)" ""
	WAIT=wait
endif

ifeq "$(INSTALL)" ""
	INSTALL=$(shell $(COMMAND) install)
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
	ifeq "$(DO_FAIL)" ""
		DO_FAIL=$(ECHO) "ok"
	endif
endif

ifeq "$(DO_FAIL)" ""
	DO_FAIL=$(shell $(COMMAND) : )
endif

ifeq "$(RM)" ""
	RM_CMD=$(shell $(COMMAND) rm)
	RM=$(RM_CMD) -f
endif

ifeq "$(RMDIR)" ""
	RMDIR=$(RM)Rd
endif

# Include the makefile
include $(FETCH_CC_INCLUDE_PATH)

.PHONY: all clean test cleanup init help clean-docs must_be_root must_have_flake must_have_pytest uninstall cleanup-dev-backups

.env:
	$(QUIET)$(ECHO) "Missing environment override."
	$(QUIET)$(ECHO) "  SHELL: '$(SHELL)'"
	$(QUIET)$(ECHO) "  LOG: '$(LOG)'"
	$(QUIET)$(ECHO) "  ERROR_LOG_PATH: '$(ERROR_LOG_PATH)'"
	$(QUIET)$(ECHO) "  QUIET: '$(QUIET)'"
	$(QUIET)$(ECHO) "  COMMAND: '$(COMMAND)'"
	$(QUIET)$(ECHO) "  MAKE: '$(MAKE)'"
	$(QUIET)$(ECHO) "  ECHO: '$(ECHO)'"
	$(QUIET)$(ECHO) "  PYTHON: '$(PYTHON)'"
	$(QUIET)$(ECHO) "  COVERAGE: '$(COVERAGE)'"
	$(QUIET)$(ECHO) "  FETCH_CC_INCLUDE_PATH: '$(FETCH_CC_INCLUDE_PATH)'"
	$(QUIET)$(ECHO) "  FETCH_CC_TOOL: '$(FETCH_CC_TOOL)'"
	$(QUIET)$(ECHO) "  CC_TOOL: '$(CC_TOOL)'"
	$(QUIET)$(ECHO) "  DS_TOOL: '$(DS_TOOL)'"
	$(QUIET)$(ECHO) "  CC_TOOL_ARGS: '$(CC_TOOL_ARGS)'"
	$(QUIET)$(ECHO) "  DS_TOOL_ARGS: '$(DS_TOOL_ARGS)'"
	$(QUIET)$(ECHO) "  PIP_ENV_FLAGS: '$(PIP_ENV_FLAGS)'"
	$(QUIET)$(ECHO) "  PIP_COMMON_FLAGS: '$(PIP_COMMON_FLAGS)'"
	$(QUIET)$(ECHO) "  DO_FAIL: '$(DO_FAIL)'"
	$(QUIET)$(ECHO) ""  # intentionally blank

MANIFEST.in: init
	$(QUIET)$(ECHO) "include requirements.txt" >"$@" ;
	$(QUIET)$(BSMARK) "$@" 2>$(ERROR_LOG_PATH) >$(ERROR_LOG_PATH) || true ;
	$(QUIET)$(ECHO) "include README.md" >>"$@" ;
	$(QUIET)$(ECHO) "include LICENSE.md" >>"$@" ;
	$(QUIET)$(ECHO) "include CHANGES.md" >>"$@" ;
	$(QUIET)$(ECHO) "include HISTORY.md" >>"$@" ;
	$(QUIET)$(ECHO) "recursive-include . *.txt" >>"$@" ;
	$(QUIET)$(ECHO) "exclude .gitignore" >>"$@" ;
	$(QUIET)$(ECHO) "exclude .deepsource.toml" >>"$@" ;
	$(QUIET)$(ECHO) "exclude .*.ini" >>"$@" ;
	$(QUIET)$(ECHO) "exclude .*.yml" >>"$@" ;
	$(QUIET)$(ECHO) "exclude .*.yaml" >>"$@" ;
	$(QUIET)$(ECHO) "global-exclude .git" >>"$@" ;
	$(QUIET)$(ECHO) "global-exclude codecov_env" >>"$@" ;
	$(QUIET)$(ECHO) "global-exclude .DS_Store" >>"$@" ;
	$(QUIET)$(ECHO) "prune .gitattributes" >>"$@" ;
	$(QUIET)$(ECHO) "prune test-reports" >>"$@" ;
	$(QUIET)$(ECHO) "prune .github" >>"$@" ;
	$(QUIET)$(ECHO) "prune .circleci" >>"$@" ;

build: init ./setup.py MANIFEST.in
	$(QUIET)$(PYTHON) -W ignore -m build --sdist --wheel --no-isolation ./ || $(QUIET)$(PYTHON) -W ignore -m build ./ ;
	$(QUIET)$(WAIT)
	$(QUIET)$(ECHO) "build DONE."

init:
	$(QUIET)$(PYTHON) -m pip install $(PIP_COMMON_FLAGS) $(PIP_ENV_FLAGS) "pip>=24.3.1" "setuptools>=75.0" "wheel>=0.44" "build>=1.1.1" 2>$(ERROR_LOG_PATH) || :
	$(QUIET)$(PYTHON) -m pip install $(PIP_COMMON_FLAGS) $(PIP_ENV_FLAGS) -r requirements.txt 2>$(ERROR_LOG_PATH) || :
	$(QUIET)$(ECHO) "$@: Done."

install: init build must_be_root
	$(QUIET)$(PYTHON) -m pip install $(PIP_COMMON_FLAGS) $(PIP_ENV_FLAGS) -e "git+https://github.com/reactive-firewall/python-repo.git#egg=pythonrepo"
	$(QUIET)$(WAIT)
	$(QUIET)$(ECHO) "$@: Done."

user-install: build
	$(QUIET)$(PYTHON) -m pip install $(PIP_COMMON_FLAGS) $(PIP_ENV_FLAGS) --user "pip>=24.3.1" "setuptools>=75.0" "wheel>=0.44" "build>=1.1.1" 2>$(ERROR_LOG_PATH) || true
	$(QUIET)$(PYTHON) -m pip install $(PIP_COMMON_FLAGS) $(PIP_ENV_FLAGS) --user -r "https://raw.githubusercontent.com/reactive-firewall/python-repo/stable/requirements.txt" 2>$(ERROR_LOG_PATH) || true
	$(QUIET)$(PYTHON) -m pip install $(PIP_COMMON_FLAGS) $(PIP_ENV_FLAGS) --user -e "git+https://github.com/reactive-firewall/python-repo.git#egg=pythonrepo"
	$(QUIET)$(WAIT)
	$(QUIET)$(ECHO) "$@: Done."

uninstall:
	$(QUIET)$(PYTHON) -m pip uninstall --use-pep517 $(PIP_ENV_FLAGS) --no-input -y pythonrepo 2>$(ERROR_LOG_PATH) || :
	$(QUIET)$(WAIT)
	$(QUIET)$(ECHO) "$@: Done."

legacy-purge: clean uninstall
	$(QUIET)$(PYTHON) -W ignore ./setup.py uninstall 2>$(ERROR_LOG_PATH) || :
	$(QUIET)$(PYTHON) -W ignore ./setup.py clean 2>$(ERROR_LOG_PATH) || :
	$(QUIET)$(RMDIR) ./build/ 2>$(ERROR_LOG_PATH) || :
	$(QUIET)$(RMDIR) ./dist/ 2>$(ERROR_LOG_PATH) || :
	$(QUIET)$(RMDIR) ./.eggs/ 2>$(ERROR_LOG_PATH) || :

purge: legacy-purge
	$(QUIET)$(RM) ./cc-test-reporter 2>$(ERROR_LOG_PATH) || :
	$(QUIET)$(RM) ./ds-cli.sh 2>$(ERROR_LOG_PATH) || :
	$(QUIET)$(RM) ./bin/deepsource 2>$(ERROR_LOG_PATH) || :
	$(QUIET)$(RMDIR) ./bin/ 2>$(ERROR_LOG_PATH) || :
	$(QUIET)$(RM) ./test-reports/*.xml 2>$(ERROR_LOG_PATH) || :
	$(QUIET)$(RMDIR) ./test-reports/ 2>$(ERROR_LOG_PATH) || :
	$(QUIET)$(ECHO) "$@: Done."

test-reports: .env
	$(QUIET)mkdir $(INST_OPTS) ./test-reports 2>$(ERROR_LOG_PATH) >$(ERROR_LOG_PATH) || true ;
	$(QUIET)$(BSMARK) ./test-reports 2>$(ERROR_LOG_PATH) >$(ERROR_LOG_PATH) || true ;
	$(QUIET)$(ECHO) "$@: Done."

test-reqs: cc-test-reporter test-reports init
	$(QUIET)$(PYTHON) -m pip install $(PIP_COMMON_FLAGS) $(PIP_ENV_FLAGS) -r tests-requirements.txt 2>$(ERROR_LOG_PATH) || true

just-test: cleanup cc-test-reporter .env
	$(QUIET)$(COVERAGE) run -p --source=pythonrepo -m unittest discover --verbose --buffer -s ./tests -t $(dir $(abspath $(lastword $(MAKEFILE_LIST)))) || $(PYTHON) -m unittest discover --verbose --buffer -s ./tests -t ./ || DO_FAIL="exit 2" ;
	$(QUIET)$(WAIT) ;
	$(QUIET)$(DO_FAIL) ;

test: just-test
	$(QUIET)$(DO_FAIL) ;
	$(QUIET)$(COVERAGE) combine 2>$(ERROR_LOG_PATH) || : ;
	$(QUIET)$(COVERAGE) report -m --include=* 2>$(ERROR_LOG_PATH) || : ;
	$(QUIET)$(CC_TOOL) $(CC_TOOL_ARGS) 2>$(ERROR_LOG_PATH) || : ;
	$(QUIET)$(ECHO) "$@: Done."

test-tox: cleanup
	$(QUIET)tox -v -- || tail -n 500 .tox/py*/log/py*.log 2>/dev/null
	$(QUIET)$(ECHO) "$@: Done."

test-pytest: cleanup MANIFEST.in cc-test-reporter must_have_pytest test-reports
	$(QUIET)$(PYTHON) -m pytest --cache-clear --doctest-glob=pythonrepo/*.py --doctest-modules --cov=. --cov-append --cov-report=xml --junitxml=test-reports/junit.xml -v --rootdir=. || DO_FAIL="exit 2" ;
	$(QUIET)$(CC_TOOL) $(CC_TOOL_ARGS) 2>$(ERROR_LOG_PATH) || : ;
	$(QUIET)$(CA_TOOL) $(CA_TOOL_ARGS) || : ;
	$(QUIET)$(DS_TOOL) $(DS_TOOL_ARGS) || : ;
	$(QUIET)$(WAIT) ;
	$(QUIET)$(DO_FAIL) ;
	$(QUIET)$(ECHO) "$@: Done."

test-style: cleanup
	$(QUIET)$(PYTHON) -m flake8 --ignore=W191,W391 --max-line-length=100 --verbose --count --config=.flake8.ini --show-source || DO_FAIL="exit 2" ;
	$(QUIET)tests/check_cc_lines 2>/dev/null || true
	$(QUIET)tests/check_spelling 2>/dev/null || true
	$(QUIET)$(ECHO) "$@: Done."

cc-test-reporter: $(FETCH_CC_INCLUDE_PATH)
	$(QUIET)$(FETCH_CC_TOOL) || DO_FAIL="exit 2" ;
	$(QUIET)$(WAIT) ;
	$(QUIET)$(DO_FAIL) ;
	$(QUIET)$(ECHO) "$@: Done."

must_have_flake:
	$(QUIET)runner=`$(PYTHON) -m pip freeze --all | grep --count -oF flake` ; \
	if test $$runner -le 0 ; then $(ECHO) "No Linter found for test." ; exit 126 ; fi

must_have_pytest: init
	$(QUIET)runner=`$(PYTHON) -m pip freeze --all | grep --count -oF pytest` ; \
	if test $$runner -le 0 ; then $(ECHO) "No python framework (pytest) found for test." ; exit 126 ; fi

cleanup-cc-test-reporter: $(FETCH_CC_INCLUDE_PATH)
	$(QUIET)$(CLEAN_CC_TOOL) || :

cleanup-dev-backups::
	$(QUIET)$(RM) ./*/*~ 2>$(ERROR_LOG_PATH) || :
	$(QUIET)$(RM) ./.*/*~ 2>$(ERROR_LOG_PATH) || :
	$(QUIET)$(RM) ./**/*~ 2>$(ERROR_LOG_PATH) || :
	$(QUIET)$(RM) ./*~ 2>$(ERROR_LOG_PATH) || :
	$(QUIET)$(RM) ./.*~ 2>$(ERROR_LOG_PATH) || :

cleanup-mac-dir-store::
	$(QUIET)$(RM) ./.DS_Store 2>$(ERROR_LOG_PATH) || :
	$(QUIET)$(RM) ./*/.DS_Store 2>$(ERROR_LOG_PATH) || :
	$(QUIET)$(RM) ./*/.DS_Store 2>$(ERROR_LOG_PATH) || :
	$(QUIET)$(RM) ./*/**/.DS_Store 2>$(ERROR_LOG_PATH) || :

cleanup-py-caches: cleanup-dev-backups cleanup-mac-dir-store
	$(QUIET)$(RM) ./*.pyc 2>$(ERROR_LOG_PATH) || :
	$(QUIET)$(RM) ./*/*.pyc 2>$(ERROR_LOG_PATH) || :
	$(QUIET)$(RM) ./*/__pycache__/* 2>$(ERROR_LOG_PATH) || :
	$(QUIET)$(RM) ./*/*/*.pyc 2>$(ERROR_LOG_PATH) || :

cleanup-py-cache-dirs: cleanup-py-caches
	$(QUIET)$(RMDIR) ./tests/__pycache__ 2>$(ERROR_LOG_PATH) || :
	$(QUIET)$(RMDIR) ./*/__pycache__ 2>$(ERROR_LOG_PATH) || :
	$(QUIET)$(RMDIR) ./*/*/__pycache__ 2>$(ERROR_LOG_PATH) || :
	$(QUIET)$(RMDIR) ./__pycache__ 2>$(ERROR_LOG_PATH) || :

cleanup-hypothesis::
	$(QUIET)$(RM) ./.hypothesis/**/* 2>$(ERROR_LOG_PATH) || true
	$(QUIET)$(RM) ./.hypothesis/* 2>$(ERROR_LOG_PATH) || true
	$(QUIET)$(RMDIR) ./.hypothesis/ 2>$(ERROR_LOG_PATH) || true

cleanup-tests: cleanup-hypothesis cleanup-py-cache-dirs cleanup-py-caches
	$(QUIET)$(RM) ./test_env/**/* 2>$(ERROR_LOG_PATH) || true
	$(QUIET)$(RM) ./test_env/* 2>$(ERROR_LOG_PATH) || true
	$(QUIET)$(RMDIR) ./test_env/ 2>$(ERROR_LOG_PATH) || true
	$(QUIET)$(RMDIR) .pytest_cache/ 2>$(ERROR_LOG_PATH) || true
	$(QUIET)$(RMDIR) ./.tox/ 2>$(ERROR_LOG_PATH) || true

cleanup-pythonrepo: cleanup-py-cache-dirs cleanup-py-caches
	$(QUIET)$(RM) pythonrepo/*.pyc 2>$(ERROR_LOG_PATH) || true
	$(QUIET)$(RM) pythonrepo/*~ 2>$(ERROR_LOG_PATH) || true
	$(QUIET)$(RM) pythonrepo/__pycache__/* 2>$(ERROR_LOG_PATH) || true
	$(QUIET)$(RM) pythonrepo/*/*.pyc 2>$(ERROR_LOG_PATH) || true

cleanup-pythonrepo-eggs: cleanup-dev-backups cleanup-mac-dir-store
	$(QUIET)$(RM) ./*.egg-info/* 2>$(ERROR_LOG_PATH) || true
	$(QUIET)$(RMDIR) ./*.egg-info 2>$(ERROR_LOG_PATH) || true
	$(QUIET)$(RMDIR) .eggs 2>$(ERROR_LOG_PATH) || true
	$(QUIET)$(RMDIR) ./.eggs/ 2>$(ERROR_LOG_PATH) || true

cleanup-src-dir: cleanup-dev-backups cleanup-mac-dir-store
	$(QUIET)$(RM) ./src/**/* 2>$(ERROR_LOG_PATH) || true
	$(QUIET)$(RM) ./src/* 2>$(ERROR_LOG_PATH) || true
	$(QUIET)$(RMDIR) ./src/ 2>$(ERROR_LOG_PATH) || true

cleanup: cleanup-tests cleanup-pythonrepo cleanup-pythonrepo-eggs cleanup-src-dir
	$(QUIET)$(RM) ./.coverage 2>$(ERROR_LOG_PATH) || true
	$(QUIET)$(RM) ./coverage*.xml 2>$(ERROR_LOG_PATH) || true
	$(QUIET)$(RM) ./sitecustomize.py 2>$(ERROR_LOG_PATH) || true
	$(QUIET)$(RMDIR) ./test-reports/ 2>$(ERROR_LOG_PATH) || true
	$(QUIET)$(WAIT) ;

build-docs: ./docs/ ./docs/Makefile docs-reqs
	$(QUIET)$(MAKE) -s -C ./docs/ -f Makefile html 2>$(ERROR_LOG_PATH) || DO_FAIL="exit 2" ;
	$(QUIET)$(WAIT) ;
	$(QUIET)mkdir $(INST_OPTS) ./docs/www 2>$(ERROR_LOG_PATH) >$(ERROR_LOG_PATH) || : ;
	$(QUIET)$(BSMARK) ./docs/www 2>$(ERROR_LOG_PATH) >$(ERROR_LOG_PATH) || : ;
	$(QUIET)$(WAIT) ;
	$(QUIET)cp -fRp ./docs/_build/ ./docs/www/ 2>$(ERROR_LOG_PATH) || DO_FAIL="exit 35" ;
	$(QUIET)$(WAIT) ;
	$(QUIET)$(MAKE) -s -C ./docs/ -f Makefile clean 2>$(ERROR_LOG_PATH) || : ;
	$(QUIET)$(WAIT) ;
	$(QUIET)$(ECHO) "Documentation should be in docs/www/html/"
	$(QUIET)$(DO_FAIL) ;

clean-docs: ./docs/ ./docs/Makefile
	$(QUIET)$(RM) ./docs/www/* 2>$(ERROR_LOG_PATH) || : ;
	$(QUIET)$(RMDIR) ./docs/www/ 2>$(ERROR_LOG_PATH) || : ;
	$(QUIET)$(MAKE) -s -C ./docs/ -f Makefile clean 2>$(ERROR_LOG_PATH) || : ;
	$(QUIET)$(WAIT) ;

./docs/:
	$(QUIET) : ;

./docs/Makefile: ./docs/
	$(QUIET)$(WAIT) ;

clean: clean-docs cleanup cleanup-cc-test-reporter
	$(QUIET)$(COVERAGE) erase 2>$(ERROR_LOG_PATH) || true
	$(QUIET)$(RM) ./test-results/junit.xml 2>$(ERROR_LOG_PATH) || true
	$(QUIET)$(RM) ./MANIFEST.in 2>$(ERROR_LOG_PATH) || true
	$(QUIET)$(ECHO) "All clean."

must_be_root:
	$(QUIET)runner=`whoami` ; \
	if test $$runner != "root" ; then echo "You are not root." ; exit 1 ; fi

%:
	$(QUIET)$(ECHO) "No Rule Found For $@" ; $(WAIT) ;

