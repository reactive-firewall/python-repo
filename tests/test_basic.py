#! /usr/bin/env python
# -*- coding: utf-8 -*-

# Python Repo Template
# ..................................
# Copyright (c) 2017-2019, Kendrick Walls
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

import sys
import unittest


class BasicTestSuite(unittest.TestCase):
	"""Basic test cases."""

	def test_absolute_truth_and_meaning(self):
		"""Insanitty Test. Because it only matters if we're not mad as hatters."""
		assert True
		self.assertTrue(True)  # skipcq: PYL-W1503

	def test_meta_test(self):
		"""Insanity Test for unittests assertion."""
		self.assertTrue(True)  # skipcq: PYL-W1503
		self.assertFalse(False)  # skipcq: PYL-W1503
		self.assertIsNone(None)

	def test_syntax(self):
		"""Test case importing pythonrepo."""
		theResult = False
		try:
			from .context import pythonrepo
			self.assertIsNotNone(pythonrepo.__name__)
			if pythonrepo.__name__ is None:
				theResult = False
			theResult = True
		except Exception as impErr:
			print(str(type(impErr)))
			print(str(impErr))
			theResult = False
		self.assertTrue(theResult)

	def test_the_help_command(self):
		"""Test case for backend library."""
		theResult = False
		try:
			from .context import pythonrepo
			self.assertIsNotNone(pythonrepo.__name__)
			if pythonrepo.__name__ is None:
				theResult = False
			with self.assertRaises(Exception):
				raise RuntimeError("This is a test")
			with self.assertRaises(Exception):
				pythonrepo.main(["--help"])
			theResult = True
		except Exception:
			theResult = False
		self.assertTrue(theResult)

	def test_corner_case_example(self):
		"""Example Test case for bad input directly into function."""
		theResult = True
		try:
			from .context import pythonrepo
			if pythonrepo.__name__ is None:
				theResult = False
			from pythonrepo import pythonrepo as _pythonrepo
			self.assertIsNone(_pythonrepo.useTool(None, None), """None, None Failed""")
			self.assertIsNone(_pythonrepo.useTool(None, []), """None, [] Failed""")
			self.assertIsNone(_pythonrepo.useTool(tool=None), """None Failed""")
			self.assertIsNone(_pythonrepo.useTool("JunkInput"), """junk Failed""")
			self.assertTrue(theResult)
		except Exception:
			self.fail("""Test Failed""")
			theResult = False
		self.assertTrue(theResult)

	def test_new_tests(self):
		"""Try adding new tests."""
		self.assertIsNone(None)
		# define new tests below

	@unittest.skipUnless(sys.platform.startswith("linux"), "This test example requires linux")
	def test_this_linux_only(self):
		"""Linux is the test."""
		self.assertTrue(sys.platform.startswith("linux"))


# leave this part
if __name__ == '__main__':
	unittest.main()
