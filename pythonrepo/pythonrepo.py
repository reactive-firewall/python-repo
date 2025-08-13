#! /usr/bin/env python3
# -*- coding: utf-8 -*-

# Python Repo Template
# ..................................
# Copyright (c) 2017-2024, Kendrick Walls
# ..................................
# Licensed under MIT (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# ..........................................
# https://www.github.com/reactive-firewall/python-repo/LICENSE.md
# ..........................................
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


__module__: str = """pythonrepo.pythonrepo"""
"""This is pythonrepo component Template."""


try:
	from . import sys
	import argparse
except Exception as err:
	# Collect Error Info
	baton = ImportError(err, str("[CWE-758] Module failed completely."))
	baton.module = __module__
	baton.path = __file__
	baton.__cause__ = err
	# Throw more relevant Error
	raise baton from err


from . import __version__ as __version__  # noqa


__prog__: str = str(__module__)
"""The name of this program is PythonRepo"""


__description__: str = str(
	"""Add a Description Here"""
)
"""Contains the description of the program."""


__epilog__: str = str(
	"""Add an epilog here."""
)
"""Contains the short epilog of the program CLI help text."""


# Add your functions here


def NoOp(*args, **kwargs) -> None:
	"""The meaning of Nothing."""
	return None


# More boiler-plate-code


TASK_OPTIONS: dict = {  # skipcq: PTC-W0020
	"noop": NoOp,
}
"""The callable function tasks of this program."""


def parseArgs(arguments=None) -> argparse.Namespace:
	"""Parses the CLI arguments.

	See `argparse.ArgumentParser` for more.

	Parameters:
		arguments (list) - the array of arguments to parse.
		Usually `sys.argv[1:]`.

	Returns:
		result (tuple(argparse.Namespace, list)) - the Namespace parsed with
		the key-value pairs.
	"""
	parser: argparse.ArgumentParser = argparse.ArgumentParser(
		prog=__prog__,
		description=__description__,
		epilog=__epilog__,
	)
	parser.add_argument(
		"some_task", choices=sorted(TASK_OPTIONS.keys()),
		help="the help text for this option."
	)
	parser.add_argument(
		"-V", "--version",
		action="version", version=f"{parser.prog} {__version__}"
	)
	return parser.parse_known_args(arguments)


def useTool(tool, *arguments) -> any:
	"""Handler for launching the functions."""
	if (tool is not None) and (tool in TASK_OPTIONS):
		try:
			TASK_OPTIONS[tool](arguments)
		except Exception:
			w = str("WARNING - An error occurred while")
			w += str("handling the tool. Abort.")
			print(w)
	else:
		return None


def main(*argv) -> None:
	"""The Main Event."""
	try:
		try:
			args, extra = parseArgs(*argv)
			service_cmd = args.some_task
			useTool(service_cmd, extra)
		except Exception as _cause:
			w = str("WARNING - An error occurred while")
			w += str("handling the arguments.")
			w += str(" Cascading failure.")
			print(w)
			raise SystemExit(2) from _cause
	except BaseException as _panic:  # nocq
		e = str("CRITICAL - An error occurred while handling")
		e += str(" the cascading failure.")
		print(e)
		raise SystemExit(3) from _panic
	sys.exit(0)


if __name__ == "__main__":
	# deepsource overlooks the readability of "if main" type code here. (See PTC-W0048)
	if (sys.argv is not None) and (len(sys.argv) >= 1):
		main(sys.argv[1:])
