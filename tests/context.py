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


__module__ = """tests.context"""
"""This is pythonrepo testing module Template."""


__module__ = """tests"""

__name__ = """tests.context"""  # skipcq: PYL-W0622

__doc__ = """

	Robust imports: These statements import the entire "pythonrepo" module,
		allowing access to all its functionalities within the test environment.
		This can be flagged as an intentional
		[cyclic-import](https://pylint.pycqa.org/en/latest/user_guide/messages/refactor/cyclic-import.html)
		warning.

	Context for Testing.

	Meta Tests - Fixtures:

		Test fixtures by importing test context.

		>>> import tests.context as context
		>>>

		>>> from context import pythonrepo as _pythonrepo
		>>>

		>>> from context import profiling as _profiling
		>>>

"""

try:
	import sys
	if not hasattr(sys, 'modules') or not sys.modules:  # pragma: no branch
		raise ModuleNotFoundError("[CWE-440] sys.modules is not available or empty.") from None
except ImportError as err:
	raise ImportError("[CWE-440] Unable to import sys module.") from err


try:
	if 'os' not in sys.modules:
		import os
	else:  # pragma: no branch
		os = sys.modules["""os"""]
except ImportError as err:  # pragma: no branch
	raise ModuleNotFoundError("[CWE-440] OS Failed to import.") from err

try:
	if 'tests.profiling' not in sys.modules:
		import tests.profiling as profiling
	else:  # pragma: no branch
		profiling = sys.modules["""tests.profiling"""]
except ImportError as err:  # pragma: no branch
	raise ModuleNotFoundError("[CWE-440] profiling Failed to import.") from err

try:
	import pythonrepo as pythonrepo  # skipcq: PYL-C0414
	if pythonrepo.__name__ is None:
		raise ImportError("Failed to import pythonrepo.")
except Exception as badErr:
	baton = ImportError(badErr, str("[CWE-758] Test module failed to load pythonrepo for test."))
	baton.module = __module__
	baton.path = __file__
	baton.__cause__ = badErr
	raise baton
