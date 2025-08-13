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


__module__ = """tests"""
"""This is pythonrepo testing module Template."""


__name__ = f"""{__module__}.context"""  # skipcq: PYL-W0622


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
	import subprocess
except ImportError as _cause:  # pragma: no branch
	raise ModuleNotFoundError("[CWE-440] subprocess Failed to import.") from _cause

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


def getCoverageCommand() -> str:
	"""
		Function for backend coverage command.
		Rather than just return the sys.executable which will usually be a python implementation,
		this function will search for a coverage tool to allow coverage testing to continue beyond
		the process fork of typical cli testing.

		Meta Testing:

		First set up test fixtures by importing test context.

			>>> import tests.context as _context
			>>>

		Testcase 1: function should have a output.

			>>> _context.getCoverageCommand() is None
			False
			>>>


	"""
	thecov = "exit 1 ; #"
	try:
		thecov = checkPythonCommand(["command", "-v", "coverage"])
		_unsafe_cov = checkPythonCommand(["which", "coverage"])
		if (str("/coverage") in str(thecov) or str("/coverage") in str(_unsafe_cov)):
			thecov = str("coverage")  # skipcq: TCV-002
		elif str("/coverage3") in str(checkPythonCommand(["command", "-v", "coverage3"])):
			thecov = str("coverage3")  # skipcq: TCV-002
		else:  # pragma: no branch
			thecov = "exit 1 ; #"  # skipcq: TCV-002
	except Exception:  # pragma: no branch
		thecov = "exit 1 ; #"  # handled error by suppressing it and indicating caller should abort.
	return str(thecov)


def __check_cov_before_py() -> str:
	"""
		Utility Function to check for coverage availability before just using plain python.
		Rather than just return the sys.executable which will usually be a python implementation,
		this function will search for a coverage tool before falling back on just plain python.

		Meta Testing:

		First set up test fixtures by importing test context.

			>>> import tests.context as _context
			>>>

		Testcase 1: function should have a output.

			>>> _context.__check_cov_before_py() is not None
			True
			>>>

		Testcase 2: function should have a string output of python or coverage.

			>>> _test_fixture = _context.__check_cov_before_py()
			>>> isinstance(_test_fixture, type(str("")))
			True
			>>> (str("python") in _test_fixture) or (str("coverage") in _test_fixture)
			True
			>>>


	"""
	thepython = str(sys.executable)
	thecov = getCoverageCommand()
	if (str("coverage") in str(thecov)) and (sys.version_info >= (3, 7)):
		thepython = str(f"{str(thecov)} run -p")  # skipcq: TCV-002
	else:  # pragma: no branch
		try:
			# pylint: disable=cyclic-import - skipcq: PYL-R0401, PYL-C0414
			import coverage as coverage  # skipcq: PYL-C0414
			if coverage.__name__ is not None:
				thepython = str("{} -m coverage run -p").format(str(sys.executable))
		except Exception:
			thepython = str(sys.executable)  # handled error by falling back on faile-safe value.
	return thepython


def getPythonCommand() -> str:
	"""
		Function for backend python command.
		Rather than just return the sys.executable which will usually be a python implementation,
		this function will search for a coverage tool with getCoverageCommand() first.

		Meta Testing:

		First set up test fixtures by importing test context.

		>>> import tests.context as _context
		>>>

		Testcase 1: function should have a output.

		>>> _context.getPythonCommand() is not None
		True
		>>>

	"""
	thepython = "python"
	try:
		thepython = __check_cov_before_py()
	except Exception:  # pragma: no branch
		thepython = "exit 1 ; #"
		try:
			thepython = str(sys.executable)
		except Exception:
			thepython = "exit 1 ; #"  # handled error by suppressing it and indicating exit.
	return str(thepython)


def taint_command_args(args: (list, tuple)) -> list:
	"""Validate and sanitize command arguments for security.

	This function validates the command (first argument) against a whitelist
	and sanitizes all arguments to prevent command injection attacks.

	Args:
		args (list): Command arguments to validate

	Returns:
		list: Sanitized command arguments

	Raises:
		CommandExecutionError: If validation fails

	Meta Testing:

		>>> import tests.context as _context
		>>> import sys as _sys
		>>>

		Testcase 1: Function should validate and return unmodified Python command.

			>>> test_fixture = ['python', '-m', 'pytest']
			>>> _context.taint_command_args(test_fixture)
			['python', '-m', 'pytest']
			>>>

		Testcase 2: Function should handle sys.executable path.

			>>> test_fixture = [str(_sys.executable), '-m', 'coverage', 'run']
			>>> result = _context.taint_command_args(test_fixture)  #doctest: +ELLIPSIS
			>>> str('python') in str(result[0]) or str('coverage') in str(result[0])
			True
			>>> result[1:] == ['-m', 'coverage', 'run']
			True
			>>>

		Testcase 3: Function should reject disallowed commands.

			>>> test_fixture = ['rm', '-rf', '/']
			>>> _context.taint_command_args(test_fixture)  #doctest: +IGNORE_EXCEPTION_DETAIL
			Traceback (most recent call last):
			ValueError: Command 'rm' is not allowed...
			>>>

		Testcase 4: Function should validate input types.

			>>> test_fixture = None
			>>> _context.taint_command_args(test_fixture)  #doctest: +IGNORE_EXCEPTION_DETAIL
			Traceback (most recent call last):
			ValueError: Invalid command arguments
			>>>
			>>> test_fixture = "python -m pytest"  # String instead of list
			>>> _context.taint_command_args(test_fixture)  #doctest: +IGNORE_EXCEPTION_DETAIL
			Traceback (most recent call last):
			ValueError: Invalid command arguments
			>>>

		Testcase 5: Function should handle coverage command variations.

			>>> test_fixture = [str(_sys.executable), 'coverage', 'run', '--source=pythonrepo']
			>>> _context.taint_command_args(test_fixture)  #doctest: +ELLIPSIS
			[...'coverage', 'run', '--source=pythonrepo']
			>>>
			>>> test_fixture = ['coverage', 'run', '--source=pythonrepo']
			>>> _context.taint_command_args(test_fixture)  #doctest: +ELLIPSIS
			['exit 1 ; #', 'run',...'run', '--source=pythonrepo']
			>>>
			>>> test_fixture = ['coverage3', 'run', '--source=.']
			>>> _context.taint_command_args(test_fixture)  #doctest: +ELLIPSIS
			['exit 1 ; #', 'run',...'--source=.']
			>>>

		Testcase 6: Function should handle case-insensitive command validation.

			>>> test_fixture = ['Python3', '-m', 'pytest']
			>>> _context.taint_command_args(test_fixture)
			['Python3', '-m', 'pytest']
			>>>
			>>> test_fixture = ['COVERAGE', 'run']
			>>> _context.taint_command_args(test_fixture)  #doctest: +ELLIPSIS
			[...'COVERAGE', 'run'...]
			>>>
	"""
	if not args or not isinstance(args, (list, tuple)):
		raise ValueError("Invalid command arguments")
	# Validate the command (first argument)
	allowed_commands = {
		"python", "python3", "coverage", "coverage3",
		sys.executable,  # Allow the current Python interpreter
	}
	command = str(args[0]).lower()
	# Extract base command name for exact matching
	# Handle both path separators (/ for Unix, \ for Windows)
	command_base = command.split("/")[-1].split("\\")[-1]
	# Check if command is allowed (exact match on base name or full path match with sys.executable)
	if command_base not in allowed_commands and command != str(sys.executable).lower():
		raise ValueError(
			f"Command '{command}' is not allowed. Allowed commands: {allowed_commands}",
		)
	# Sanitize all arguments to prevent injection
	tainted_args = [str(arg) for arg in args]
	# Special handling for coverage commands
	if "coverage" in command:
		tainted_args = checkCovCommand(*tainted_args)
	# Sanitize all arguments to prevent injection
	return tainted_args


def validateCommandArgs(args: list) -> None:
	"""
	Validates command arguments to ensure they do not contain null characters.

	Args:
		args (list): A list of command arguments to be validated.

	Raises:
		ValueError: If any argument contains a null character.
	"""
	if (args is None) or (args == [None]) or (len(args) <= 0):  # pragma: no branch
		# skipcq: TCV-002
		raise ValueError("[CWE-1286] args must be an array of positional arguments") from None
	for arg in args:
		if isinstance(arg, str) and "\x00" in arg:
			raise ValueError("[CWE-20] Null characters are not allowed in command arguments.")


def checkStrOrByte(theInput):
	"""
	Converts the input to a string if possible, otherwise returns it as bytes.

	This utility function is designed to handle both string and byte inputs,
	ensuring consistent output type. It attempts to decode byte inputs to UTF-8
	strings, falling back to bytes if decoding fails.

	Args:
		theInput: The input to be checked and potentially converted.
					Can be None, str, bytes, or any other type.

	Returns:
		str: If the input is already a string or can be decoded to UTF-8.
		bytes: If the input is bytes and cannot be decoded to UTF-8.
		None: If the input is None.

	Meta Testing:

		First set up test fixtures by importing test context.

			>>> import tests.context as _context
			>>>

		Testcase 1: Input is a string.

			>>> _context.checkStrOrByte("Hello")
			'Hello'
			>>>

		Testcase 2: Input is UTF-8 decodable bytes.

			>>> _context.checkStrOrByte(b"Hello")
			'Hello'
			>>>

		Testcase 3: Input is bytes that are not UTF-8 decodable.

			>>> _context.checkStrOrByte(b'\\xff\\xfe')
			b'\xff\xfe'
			>>>

		Testcase 4: Input is None.

			>>> _context.checkStrOrByte(None) is None
			True
			>>>

		Testcase 5: Input is an empty string.

			>>> _context.checkStrOrByte("")
			''
			>>>

		Testcase 6: Input is empty bytes.

			>>> _context.checkStrOrByte(b"")
			''
			>>>


	"""
	theOutput = None
	if theInput is not None:  # pragma: no branch
		theOutput = theInput
	try:
		if isinstance(theInput, bytes):
			theOutput = theInput.decode("UTF-8")
	except UnicodeDecodeError:  # pragma: no branch
		theOutput = bytes(theInput)
	return theOutput


def checkCovCommand(*args):  # skipcq: PYL-W0102  - [] != [None]
	"""
	Modifies the input command arguments to include coverage-related options when applicable.

	This utility function checks if the first argument contains "coverage" and, if so,
	modifies the argument list to include additional coverage run options. It's primarily
	used internally by other functions in the testing framework.
	Not intended to be run directly.

	Args:
		*args (list): A list of command arguments; should not be pass None.

	Returns:
		list: The modified list of arguments with 'coverage run' options added as applicable.

	Meta Testing:

		First set up test fixtures by importing test context.

			>>> import tests.context as _context
			>>>

		Testcase 1: Function should return unmodified arguments if 'coverage' is missing.

			>>> _context.checkCovCommand("python", "script.py")
			['python', 'script.py']

		Testcase 2: Function should modify arguments when 'coverage' is the first argument.
			A.) Missing 'run'

			>>> _context.checkCovCommand("coverage", "script.py")  #doctest: +ELLIPSIS
			['...', 'run', '-p', '--context=Integration', '--source=pythonrepo', 'script.py']

		Testcase 3: Function should modify arguments when 'coverage run' is in the first argument.
			A.) NOT missing 'run'

			>>> _context.checkCovCommand("coverage run", "script.py")  #doctest: +ELLIPSIS
			['...', 'run', '-p', '--context=Integration', '--source=pythonrepo', 'script.py']

		Testcase 4: Function should handle coverage command with full path.

			>>> _context.checkCovCommand("/usr/bin/coverage", "test.py")  #doctest: +ELLIPSIS
			['...', 'run', '-p', '--context=Integration', '--source=pythonrepo', 'test.py']

		Testcase 5: Function should handle coverage invoked via sys.executable.

			>>> import sys as _sys
			>>> test_fixture = [str("{} -m coverage run").format(_sys.executable), "test.py"]
			>>> _context.checkCovCommand(*test_fixture)  #doctest: +ELLIPSIS
			[..., '-m', 'coverage', 'run', '-p', '...', '--source=pythonrepo', 'test.py']


	"""
	if sys.__name__ is None:  # pragma: no branch
		raise ImportError("[CWE-758] Failed to import system.") from None
	if not args or args[0] is None:
		# skipcq: TCV-002
		raise ValueError("[CWE-1286] args must be an array of positional arguments") from None
	else:
		args = [*args]  # convert to an array
	if str("coverage") in args[0]:
		i = 1
		if str(f"{str(sys.executable)} -m coverage") in str(args[0]):  # pragma: no branch
			args[0] = str(sys.executable)
			args.insert(1, str("-m"))
			args.insert(2, str("coverage"))
			i += 2
		else:  # pragma: no branch
			args[0] = str(getCoverageCommand())
		extra_args = ["run", "-p", "--context=Integration", "--source=pythonrepo"]
		# PEP-279 - see https://www.python.org/dev/peps/pep-0279/
		for k, ktem in enumerate(extra_args):
			offset = i + k
			args.insert(offset, ktem)
	return [*args]


def checkPythonCommand(args, stderr=None):
	"""
	Execute a Python command and return its output.

	This function is a wrapper around subprocess.check_output with additional
	error handling and output processing. It's designed to execute Python
	commands or coverage commands, making it useful for running tests and
	collecting coverage data.

	Args:
		args (list): A list of command arguments to be executed.
		stderr (Optional[int]): File descriptor for stderr redirection.
			Defaults to None.

	Returns:
		str: The command output as a string, with any byte output decoded to UTF-8.

	Raises:
		subprocess.CalledProcessError: If the command returns a non-zero exit status.

	Meta Testing:

		First set up test fixtures by importing test context.

			>>> import sys as _sys
			>>> import tests.context as _context
			>>>

		Testcase 1: Function should have an output when provided valid arguments.

			>>> test_fixture_1 = [str(_sys.executable), '-c', 'print("Hello, World!")']
			>>> _context.checkPythonCommand(test_fixture_1)
			'Hello, World!\\n'

		Testcase 2: Function should capture stderr when specified.

			>>> import subprocess as _subprocess
			>>> test_args_2 = [
			... 	str(_sys.executable), '-c', 'import sys; print("Error", file=sys.stderr)'
			... ]
			>>>
			>>> _context.checkPythonCommand(test_args_2, stderr=_subprocess.STDOUT)
			'Error\\n'

		Testcase 3: Function should handle exceptions and return output.

			>>> test_fixture_e = [str(_sys.executable), '-c', 'raise ValueError("Test error")']
			>>> _context.checkPythonCommand(
			... 	test_fixture_e, stderr=_subprocess.STDOUT
			... ) #doctest: +ELLIPSIS
			'Traceback (most recent call last):\\n...ValueError...'

		Testcase 4: Function should return the output as a string.

			>>> test_fixture_s = [str(_sys.executable), '-c', 'print(b"Bytes output")']
			>>> isinstance(_context.checkPythonCommand(
			... 	test_fixture_s, stderr=_subprocess.STDOUT
			... ), str)
			True


	"""
	theOutput = None
	try:
		if (args is None) or (args == [None]) or (len(args) <= 0):  # pragma: no branch
			theOutput = None  # None is safer than subprocess.check_output(["exit 1 ; #"])
		else:
			validateCommandArgs(args)
			if str("coverage") in args[0]:
				args = checkCovCommand(*args)
			# Validate and sanitize command arguments
			safe_args = taint_command_args(args)
			theOutput = subprocess.check_output(safe_args, stderr=stderr)
	except Exception as _cause:  # pragma: no branch
		theOutput = None
		try:
			if _cause.output is not None:
				theOutput = _cause.output
		except Exception:
			theOutput = None  # suppress all errors
	theOutput = checkStrOrByte(theOutput)
	return theOutput
