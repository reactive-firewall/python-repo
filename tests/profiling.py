#! /usr/bin/env python
# -*- coding: utf-8 -*-

# Python Test Repo Template
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

# Third-party Acknowledgement:
# ..........................................
# Some code (namely: class timewith, @do_cprofile, @do_line_profile) was modified/derived from:
# https://github.com/zapier/profiling-python-like-a-boss/tree/1ab93a1154
# Copyright (c) 2013, Zapier Inc. All rights reserved.
# which was under BSD-3 Clause license.
# see https://github.com/zapier/profiling-python-like-a-boss/blob/1ab93a1154/LICENSE.md for details
# ..........................................
# NO ASSOCIATION

__module__ = """tests.profiling"""
"""This is pythonrepo testing module Template."""

try:
	import sys
	if sys.__name__ is None:  # pragma: no branch
		raise ImportError("[CWE-758] OMG! we could not import sys! ABORT. ABORT.")
except Exception as badErr:  # pragma: no branch
	baton = ImportError(badErr, str("[CWE-758] Test module failed completely."))
	baton.module = __module__
	baton.path = __file__
	baton.__cause__ = badErr
	raise baton

try:
	if 'os' not in sys.modules:
		import os
	else:  # pragma: no branch
		os = sys.modules["""os"""]
except Exception as badErr:  # pragma: no branch
	baton = ImportError(badErr, str("[CWE-758] Test module failed completely."))
	baton.module = __module__
	baton.path = __file__
	baton.__cause__ = badErr
	raise baton

try:
	if 'functools' not in sys.modules:
		import functools
	else:  # pragma: no branch
		functools = sys.modules["""functools"""]
except Exception as badErr:  # pragma: no branch
	baton = ImportError(badErr, str("[CWE-758] Test module failed completely."))
	baton.module = __module__
	baton.path = __file__
	baton.__cause__ = badErr
	raise baton

try:
	import time
	if time.__name__ is None:  # pragma: no branch
		raise NotImplementedError("[CWE-440] We could not import time. Are we in the speed-force!")
except Exception as badErr:  # pragma: no branch
	baton = ImportError(badErr, str("[CWE-758] Test module failed completely."))
	baton.module = __module__
	baton.path = __file__
	baton.__cause__ = badErr
	raise baton

try:
	if 'cProfile' not in sys.modules:
		import cProfile
	else:  # pragma: no branch
		cProfile = sys.modules["""cProfile"""]
except Exception as badErr:  # pragma: no branch
	baton = ImportError(badErr, str("[CWE-758] Test module failed completely."))
	baton.module = __module__
	baton.path = __file__
	baton.__cause__ = badErr
	raise baton

try:
	try:
		sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), str('..'))))
		sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), str('.'))))
	except Exception as ImportErr:  # pragma: no branch
		raise ImportError(ImportErr, str("[CWE-758] Profile module failed completely."))
except Exception as badErr:  # pragma: no branch
	baton = ImportError(badErr, str("[CWE-758] Test module failed completely."))
	baton.module = __module__
	baton.path = __file__
	baton.__cause__ = badErr
	raise baton


class timewith():
	"""Basic timer for do_time_profile."""
	def __init__(self, name=''):
		self.name = name
		self.start = time.time()

	@property
	def elapsed(self):
		return time.time() - self.start

	def checkpoint(self, name=''):
		print(
			str("{timer} {checkpoint} took {elapsed} seconds").format(
				timer=self.name,
				checkpoint=name,
				elapsed=self.elapsed,
			).strip()
		)

	def __enter__(self):
		return self

	def __exit__(self, type, value, traceback):  # skipcq: PYL-W0622
		self.checkpoint(str("finished"))


def do_time_profile(func, timer_name="time_profile"):
	"""Run a function with a timer.

	Time Testing:

		First some test fixtures:

		>>> import tests.context as context
		>>> from context import profiling as profiling
		>>>

	Testcase 0: test the time_profile.

		>>> def doWork():
		...    \"""Does some work.\"""
		...    for i in range(0, 42):
		...        print(str("Do Task {}").format(int(i)))
		>>>
		>>> profiling.do_time_profile(
		...    doWork,
		...    timer_name=str("work time test")
		... )() #doctest: -DONT_ACCEPT_BLANKLINE, +ELLIPSIS
		work...Start Timer...
		...Do Task...
		work...Stop Timer...
		work...took ... seconds
		>>>

	"""
	@functools.wraps(func)
	def timer_profile_func(*args, **kwargs):
		"""Wraps a function in timewith() function."""
		theOutput = None
		with timewith(timer_name) as timer:
			timer.checkpoint(str("Start Timer"))
			theOutput = func(*args, **kwargs)
			timer.checkpoint(str("Stop Timer"))
		return theOutput

	return timer_profile_func


def do_cprofile(func):
	"""Use built-in profiler to profile.

	Time Testing:

		First some test fixtures:

		>>> import tests.context as context
		>>> from context import profiling as profiling
		>>>

	Testcase 0: test the time_profile.

		>>> def doWork():
		...    \"""Does some work.\"""
		...    for i in range(0, 42):
		...        print(str("Do Task {}").format(int(i)))
		>>>
		>>> profiling.do_cprofile(
		...    doWork
		... )() #doctest: -DONT_ACCEPT_BLANKLINE, +ELLIPSIS
		Do Task 0...Do Task 10...Do Task 20...Do Task 30...Do Task 40...
		...function calls in ... seconds...Ordered by: standard name...
		...ncalls  tottime  percall  cumtime  percall filename:lineno(function)...
		...<...>:1(doWork)...{built-in method builtins.print}...
		<BLANKLINE>
		<BLANKLINE>
		>>>


	"""
	@functools.wraps(func)
	def profiled_func(*args, **kwargs):
		"""Wraps a function in profile.enable/disable() functions."""
		profile = cProfile.Profile()
		try:
			profile.enable()
			result = func(*args, **kwargs)
			profile.disable()
			return result
		finally:
			profile.print_stats()

	return profiled_func


try:  # noqa
	from line_profiler import LineProfiler

	def do_profile(follow=None):  # pragma: no cover
		if follow is None:
			follow = []

		def inner(func):
			def profiled_func(*args, **kwargs):
				try:
					profiler = LineProfiler()
					profiler.add_function(func)
					for f in follow:
						profiler.add_function(f)
					profiler.enable_by_count()
					return func(*args, **kwargs)
				finally:
					profiler.print_stats()

			return profiled_func

		return inner

except ImportError:  # pragma: no cover

	def do_profile(follow=None):
		"""Helpful if you accidentally leave in production!"""
		if follow is None:
			follow = []

		def inner(func):
			def nothing(*args, **kwargs):
				return func(*args, **kwargs)

			return nothing

		return inner


def main(*argv):  # pragma: no cover
	"""The Main Event makes no sense to profiling."""
	raise NotImplementedError("CRITICAL - test profiling main() not implemented. yet?")


if __name__ in '__main__':  # pragma: no cover
	exitcode = 3
	try:
		exitcode = main(sys.argv[1:])
	finally:
		sys.exit(exitcode)
