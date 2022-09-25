# -*- coding: utf-8 -*-

# Python Repo Template
# ..................................
# Copyright (c) 2017-2022, Kendrick Walls
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


try:
	import sys
	import os
	if 'pythonrepo' in __file__:
		sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
except Exception as badErr:
	baton = ImportError(badErr, str("[CWE-758] Test module failed completely."))
	baton.module = __module__
	baton.path = __file__
	baton.__cause__ = badErr
	raise baton


try:
	import pythonrepo as pythonrepo
	if pythonrepo.__name__ is None:
		raise ImportError("Failed to import pythonrepo.")
except Exception as badErr:
	baton = ImportError(badErr, str("[CWE-758] Test module failed to load pythonrepo for test."))
	baton.module = __module__
	baton.path = __file__
	baton.__cause__ = badErr
	raise baton
