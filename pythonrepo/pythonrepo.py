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
# https://www.github.com/reactive-firewall/python-repo/LICENSE.md
# ..........................................
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


try:
	import sys
	import argparse
except Exception as err:
	# Show Error Info
	print(str(type(err)))
	print(str(err))
	print(str(err.args))
	print(str(""))
	# Clean up Error
	err = None
	del(err)
	# Throw more relevant Error
	raise ImportError(str("Error Importing Python"))


__prog__ = str("""pythonrepo""")
"""The name of this program is PythonRepo"""


__description__ = str(
	"""Add a Description Here"""
)
"""Contains the description of the program."""


__epilog__ = str(
	"""Add an epilog here."""
)
"""Contains the short epilog of the program CLI help text."""


__version__ = """1.1.1"""
"""The version of this program."""


# Add your functions here


def NoOp(*args, **kwargs):
	"""The meaning of Nothing."""
	return None


# More boiler-plate-code


TASK_OPTIONS = dict({
	'noop': NoOp
})
"""The callable function tasks of this program."""


def parseArgs(arguments=None):
	"""Parses the CLI arguments. See argparse.ArgumentParser for more.
	param str - arguments - the array of arguments to parse.
		Usually sys.argv[1:]
	returns argparse.Namespace - the Namespace parsed with
		the key-value pairs.
	"""
	parser = argparse.ArgumentParser(
		prog=__prog__,
		description=__description__,
		epilog=__epilog__
	)
	parser.add_argument(
		'some_task', choices=TASK_OPTIONS.keys(),
		help='the help text for this option.'
	)
	parser.add_argument(
		'-V', '--version',
		action='version', version=str(
			"%(prog)s {version}"
		).format(version=str(__version__))
	)
	return parser.parse_known_args(arguments)


def __checkToolArgs(args=None):
	"""Handles None case for arguments as a helper function."""
	if args is None:
		args = [None]
	return args


def useTool(tool, arguments=None):
	"""Handler for launching the functions."""
	arguments = __checkToolArgs(arguments)
	if (tool is not None) and (tool in TASK_OPTIONS.keys()):
		try:
			# print(str("launching: " + tool))
			TASK_OPTIONS[tool](arguments)
		except Exception:
			w = str("WARNING - An error occured while")
			w += str("handling the tool. Abort.")
			print(w)
	else:
		return None


def main(argv=None):
	"""The Main Event."""
	try:
		try:
			args, extra = parseArgs(argv)
			service_cmd = args.some_task
			useTool(service_cmd, extra)
		except Exception:
			w = str("WARNING - An error occured while")
			w += str("handling the arguments.")
			w += str(" Cascading failure.")
			print(w)
			exit(2)
	except Exception:
		e = str("CRITICAL - An error occured while handling")
		e += str("the cascading failure.")
		print(e)
		exit(3)
	exit(0)


if __name__ == '__main__':
	if (sys.argv is not None) and (len(sys.argv) >= 1):
		main(sys.argv[1:])
