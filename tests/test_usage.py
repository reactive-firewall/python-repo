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


import unittest
import subprocess
import sys
import tests.profiling as profiling

from tests.context import (
	getPythonCommand,
	checkPythonCommand,
)


@profiling.do_cprofile
def timePythonCommand(args=None, stderr=None):
	"""
	Function for backend subprocess check_output command
	with support for coverage and profiling.
	"""
	if args is None:
		args = [None]
	return checkPythonCommand(args, stderr)


def debugBlob(blob=None):
	"""In case you need it."""
	try:
		print(str(""))
		print(str("String:"))
		print(str("""\""""))
		print(str(blob))
		print(str("""\""""))
		print(str(""))
		print(str("Raw:"))
		print(str("""\""""))
		print(repr(blob))
		print(str("""\""""))
		print(str(""))
	except Exception:
		return False
	return True


def debugIfNoneResult(thepython, theArgs, theOutput):
	"""In case you need it."""
	try:
		if not (str(theOutput) is None or str(theOutput) == str(None)):
			theResult = True
		else:
			theResult = False
			print(str(""))
			print(str("python exe is {}").format(str(sys.executable)))
			print(str("python cmd used is {}").format(str(thepython)))
			print(str("arguments used were {}").format(str(theArgs)))
			print(str(""))
			print(str("actual output was..."))
			print(str(""))
			print(str("{}").format(str(theOutput)))
			print(str(""))
	except Exception:
		theResult = False
	return theResult


class BasicUsageTestSuite(unittest.TestCase):
	"""Basic functional test cases."""

	def test_absolute_truth_and_meaning(self):
		"""Insanity Test. if ( is true ) usage."""
		self.assertTrue(True)  # skipcq: PYL-W1503

	def test_syntax(self):
		"""Test case importing code. if ( import is not None ) usage."""
		theResult = False
		try:
			from .context import pythonrepo
			if pythonrepo.__name__ is None:
				theResult = False
			theResult = True
		except Exception as impErr:
			print(str(type(impErr)))
			print(str(impErr))
			theResult = False
		self.assertTrue(theResult)

	def test_template_case(self):
		"""Test case template for: python -m pythonrepo.* --version usage."""
		theResult = False
		thepython = getPythonCommand()
		if (thepython is not None):
			try:
				for test_case in ["pythonrepo"]:
					args = [
						str(thepython),
						str("-m"),
						str("pythonrepo.{}").format(
							str(
								test_case
							)
						),
						str("--version")
					]
					theOutputtext = checkPythonCommand(args, stderr=subprocess.STDOUT)
					# now test it
					try:
						if isinstance(theOutputtext, bytes):
							theOutputtext = theOutputtext.decode('utf8')
					except UnicodeDecodeError:
						theOutputtext = str(repr(bytes(theOutputtext)))
					# ADD REAL VERSION TEST HERE
					theResult = debugIfNoneResult(thepython, args, theOutputtext)
					self.assertTrue(theResult)
					# or simply:
					self.assertIsNotNone(theOutputtext)
			except Exception as err:
				self.fail(err)
				err = None
				del err  # skipcq: PTC-W0043
				theResult = False
		self.assertTrue(theResult)

	def test_profile_template_case(self):
		"""Test case template for profiling."""
		theResult = False
		thepython = getPythonCommand()
		if (thepython is not None):
			try:
				for test_case in ["noop"]:
					args = [
						str(thepython),
						str("-m"),
						str("pythonrepo.pythonrepo"),
						str("{}").format(
							str(
								test_case
							)
						)
					]
					theOutputtext = timePythonCommand(args, stderr=subprocess.STDOUT)
					# now test it
					try:
						if isinstance(theOutputtext, bytes):
							theOutputtext = theOutputtext.decode('utf8')
					except UnicodeDecodeError:
						theOutputtext = str(repr(bytes(theOutputtext)))
					theResult = debugIfNoneResult(thepython, args, theOutputtext)
					# or simply:
					self.assertIsNotNone(theOutputtext)
			except Exception as err:
				self.fail(err)
				err = None
				del err  # skipcq: PTC-W0043
				theResult = False
		self.assertTrue(theResult)

	@unittest.expectedFailure
	def test_fail_template_case(self):
		"""Test case template for profiling with an expected failure."""
		theResult = False
		thepython = getPythonCommand()
		if (thepython is not None):
			try:
				for test_case in ["BadInput"]:
					args = [
						str(thepython),
						str("-m"),
						str("pythonrepo.pythonrepo"),
						str("{}").format(
							str(
								test_case
							)
						)
					]
					theOutputtext = timePythonCommand(args, stderr=subprocess.STDOUT)
					# now test it
					try:
						if isinstance(theOutputtext, bytes):
							theOutputtext = theOutputtext.decode('utf8')
					except UnicodeDecodeError:
						theOutputtext = str(repr(bytes(theOutputtext)))
					theResult = not debugIfNoneResult(thepython, args, theOutputtext)
					# or simply:
					self.assertIsNone(theOutputtext)
			except Exception as err:
				self.fail(err)
				err = None
				del err  # skipcq: PTC-W0043
				theResult = False
		self.assertTrue(theResult)

	def test_bad_template_case(self):
		"""Test case template for profiling."""
		theResult = False
		thepython = getPythonCommand()
		if (thepython is not None):
			try:
				for test_case in [None]:
					args = [
						str(thepython),
						str("-m"),
						str("pythonrepo.pythonrepo"),
						str("{}").format(
							str(
								test_case
							)
						)
					]
					theOutputtext = timePythonCommand(args, stderr=subprocess.STDOUT)
					# now test it
					try:
						if isinstance(theOutputtext, bytes):
							theOutputtext = theOutputtext.decode('utf8')
					except UnicodeDecodeError:
						theOutputtext = str(repr(bytes(theOutputtext)))
					theResult = debugIfNoneResult(thepython, args, theOutputtext)
					# or simply:
					self.assertIsNotNone(theOutputtext)
			except Exception as err:
				self.fail(err)
				err = None
				del err  # skipcq: PTC-W0043
				theResult = False
		self.assertTrue(theResult)


if __name__ == '__main__':
	unittest.main()

