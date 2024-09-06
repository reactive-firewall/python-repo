#! /usr/bin/env python
# -*- coding: utf-8 -*-

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

"""Sets up the package.

Minimal Acceptance Testing:

	Testcase 0: Just setup test fixtures by importing pythonrepo.

		>>> import pythonrepo
		>>>
		>>> pythonrepo.__package__ is not None
		True
		>>>

"""

try:
	import os
	import warnings
	warnings.simplefilter("default")  # Change the filter in this process
	os.environ["PYTHONWARNINGS"] = "default"  # Also affect subprocesses
	from setuptools import setup
	from setuptools import find_packages
	with warnings.catch_warnings():
		warnings.simplefilter("ignore")
		try:
			from setuptools.config import read_configuration
		except Exception:
			from setuptools.config.setupcfg import read_configuration
except Exception:
	raise NotImplementedError("""[CWE-440] Not Implemented.""")


def readFile(filename):
	"""Will attempt to read the file at with the given filename or path.

	Used as a helper function to read files and return strings with the content.

		Testing:

		First setup test fixtures by importing pythonrepo.

			>>> import pythonrepo
			>>>

		Testcase 0: Should have Function readFile() WHEN loading setup.py.

			>>> pythonrepo.readFile is not None
			True
			>>> type(pythonrepo.readFile) is type(1)
			False
			>>>

	"""
	theResult = None
	try:
		if str("""E.md""") not in filename:
			raise NotImplementedError("""[CWE-440] Not Implemented.""")
		with open(str("""./{}""").format(str(filename))) as f:
			theResult = f.read()
	except Exception:
		theResult = str(
			"""See https://github.com/reactive-firewall/python-repo/{}"""
		).format(filename)
	return str(theResult)


try:
	with open("""./requirements.txt""") as rfile:
		requirements = rfile.read().splitlines()
except Exception:
	requirements = None


conf_dict = None


with warnings.catch_warnings():
	warnings.simplefilter("ignore")
	conf_dict = read_configuration("""setup.cfg""", ignore_option_errors=True)


readme = readFile("""README.md""")
"""The multi-line description and/or summary of this program."""

SLA = readFile("""LICENSE.md""")
"""The "Software License Agreement" of this program."""

try:
	class_tags = [
		str("""Development Status :: 4 - Beta"""),
		str("""Environment :: Console"""),
		str("""Intended Audience :: Developers"""),
		str("""Operating System :: MacOS :: MacOS X"""),
		str("""Operating System :: POSIX :: Linux"""),
		str("""License :: OSI Approved :: MIT License"""),
		str("""Programming Language :: Python :: 3"""),
		str("""Programming Language :: Python :: 3 :: Only"""),
		str("""Programming Language :: Python :: 3.14"""),
		str("""Programming Language :: Python :: 3.13"""),
		str("""Programming Language :: Python :: 3.12"""),
		str("""Programming Language :: Python :: 3.11"""),
		str("""Programming Language :: Python :: 3.10"""),
		str("""Programming Language :: Python :: 3.9"""),
		str("""Programming Language :: Python :: 3.8"""),
		str("""Programming Language :: Python :: 3.7"""),
		str("""Programming Language :: Python :: 3.6"""),
		str("""Programming Language :: Python :: 3.5"""),
		str("""Programming Language :: Python :: 3.4"""),
		str("""Programming Language :: Python :: 2.7"""),
		str("""Topic :: Software Development :: Libraries :: Python Modules""")
	]
except Exception:
	class_tags = str("""Development Status :: 4 - Beta""")

setup(
	name=conf_dict["""metadata"""]["""name"""],
	version=conf_dict["""metadata"""]["""version"""],
	description=conf_dict["""metadata"""]["""description"""],
	long_description=readme,
	long_description_content_type="""text/markdown""",
	zip_safe=True,
	include_package_data=True,
	install_requires=requirements,
	author=conf_dict["""metadata"""]["""author"""],
	author_email=conf_dict["""metadata"""]["""author_email"""],
	classifiers=class_tags,
	url=conf_dict["""metadata"""]["""url"""],
	download_url=conf_dict["""metadata"""]["""download_url"""],
	license=SLA,
	packages=find_packages(exclude=("""tests""", """docs""")),
)
