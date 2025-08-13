# -*- coding: utf-8 -*-

# Python Repo Template
# ..................................
# Copyright (c) 2017-2025, Mr. Walls
# ..................................
# Licensed under MIT (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# ..........................................
# https://github.com/reactive-firewall/python-repo/LICENSE.md
# ..........................................
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Python Repo Testing Module."""

__module__: str = """tests"""
"""This is pythonrepo testing module Template."""


try:
	try:
		import sys
		import os
		sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), str('..'))))
	except (ImportError, OSError, TypeError, ValueError, AttributeError, IndexError) as ImportErr:
		raise ImportError("[CWE-758] Test module failed completely.") from ImportErr
	from tests import context as context  # skipcq: PYL-C0414
	if not hasattr(context, '__name__') or not context.__name__:  # pragma: no branch
		raise ImportError("[CWE-758] Failed to import context") from None
	from tests import profiling as profiling  # skipcq: PYL-C0414
	if not hasattr(profiling, '__name__') or not profiling.__name__:  # pragma: no branch
		raise ImportError("[CWE-758] Failed to import the profiling framework.") from None
	from tests import test_basic
	if not hasattr(test_basic, '__name__') or not test_basic.__name__:  # pragma: no branch
		raise ImportError("[CWE-758] Failed to import the basic tests.") from None
except Exception as badErr:
	baton = ImportError(badErr, str("[CWE-758] Test module failed completely."))
	baton.module = __module__
	baton.path = __file__
	baton.__cause__ = badErr
	raise baton
