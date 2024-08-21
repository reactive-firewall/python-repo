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

"""Python Repo Testing Module."""

__module__ = """tests"""
"""This is pythonrepo testing module Template."""


try:
	try:
		import sys
		import os
		sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), str('..'))))
	except Exception as ImportErr:
		print(str(''))
		print(str(type(ImportErr)))
		print(str(ImportErr))
		print(str((ImportErr.args)))
		print(str(''))
		ImportErr = None
		del ImportErr
		raise ImportError(str("Test module failed completely."))
	from tests import context as context  # skipcq: PYL-C0414
	if context.__name__ is None:
		raise ImportError(str("Test module failed to import even the context framework."))
	from tests import profiling as profiling  # skipcq: PYL-C0414
	if profiling.__name__ is None:
		raise ImportError(str("Test module failed to import even the profiling framework."))
	from tests import test_basic
	if test_basic.__name__ is None:
		raise ImportError(str("Test module failed to import even the basic tests."))
except Exception as badErr:
	baton = ImportError(badErr, str("[CWE-758] Test module failed completely."))
	baton.module = __module__
	baton.path = __file__
	baton.__cause__ = badErr
	raise baton
