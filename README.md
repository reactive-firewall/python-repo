# About
This repo is basically my template for new repos/projects

# CI Template:

By default this template will assume that the Travis CI Service is used for CI/CD

# Status

### master:
[![status](https://travis-ci.org/reactive-firewall/python-repo.svg?branch=master)](https://travis-ci.org/reactive-firewall/python-repo)
[![code coverage](https://codecov.io/gh/reactive-firewall/python-repo/branch/master/graph/badge.svg)](https://codecov.io/gh/reactive-firewall/python-repo/branch/master/)

### Stable:
[![status](https://travis-ci.org/reactive-firewall/python-repo.svg?branch=stable)](https://travis-ci.org/reactive-firewall/python-repo)
[![code coverage](https://codecov.io/gh/reactive-firewall/python-repo/branch/stable/graph/badge.svg)](https://codecov.io/gh/reactive-firewall/python-repo/branch/stable/)

# How do I use this to create a new project repo?

(assuming new project is already forked on github to `MY-NEW-REPO`)

```bash
# cd /MY-AWSOME-DEV-PATH
git clone https://github.com/reactive-firewall/MY-NEW-REPO.git MY-NEW-REPO
# cd ./MY-NEW-REPO
```

# Dev Testing Template:

In a rush? Then use this:

```bash
make clean ; # cleans up from any previous tests hopefully
make test ; # runs the tests
make clean ; # cleans up for next test
```

Use PEP8 to check code style? Great! Try this:

```bash
make clean ; # cleans up from any previous tests hopefully
make test-style ; # runs the tests
make clean ; # cleans up for next test
```

Want more tests? Cool! Try `tox`:

```bash
make clean ; # cleans up from any previous tests hopefully
make test-tox ; # runs the tox tests
make clean ; # cleans up for next test
```

# License - MIT

## Copyright (c) 2017 Mr. Walls
### 
### THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
### IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
### FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
### AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
### LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
### OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
### SOFTWARE.
###
### Permission is hereby granted, free of charge, to any person obtaining a copy
### of this software and associated documentation files (the "Software"), to deal
### in the Software without restriction, including without limitation the rights
### to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
### copies of the Software, and to permit persons to whom the Software is
### furnished to do so, subject to the following conditions:
###
### The above copyright notice and this permission notice shall be included in all
### copies or substantial portions of the Software.

## USE AT OWN RISK.

