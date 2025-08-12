#! /usr/bin/env python3
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

"""Python Repo."""

__module__: str = """pythonrepo"""
"""This is pythonrepo module Template."""


__version__: str = """2.0.0"""
"""This is version 2.0.0 of pythonrepo Template"""


try:
	import sys
	import os
	if str(__module__) in __file__:  # pragma: no branch
		__parentPath: str = os.path.join(
			os.path.dirname(__file__), "..",
		)
		if str(os.path.abspath(__parentPath)) not in sys.path:  # pragma: no branch
			sys.path.insert(0, os.path.abspath(__parentPath))
except ImportError as err:
	baton = ImportError(err, str("[CWE-758] Module failed completely."))
	baton.module = __module__
	baton.path = __file__
	baton.__cause__ = err
	raise baton from err
