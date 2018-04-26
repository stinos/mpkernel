[![Build Status](https://travis-ci.org/TDAbboud/mpkernel.svg?branch=master)](https://travis-ci.org/TDAbboud/mpkernel)

# mpkernel

> An experimental Jupyter kernel for micropython

## Requirements

* Python 3.4+
* Jupyter  >= 1.0.0
* pyserial >= 2.7   (for stmhal kernel)
 
## Installation

Make sure you have the packages under requirements installed then run the following::

```bash
$ git clone https://github.com/TDAbboud/mpkernel.git
$ cd mpkernel
$ make install
```

<!---
 Future pip installation
    The easiest way to install mpkernel is with pip::

    $ pip install mpkernel

    This will install kernels for the unix (`mpunix`) and stmhal(`mpstmhal`) port

    See its `Python Package Index entry`_ for more.
-->

## Unix port

Build with standard readline, patch:
```
--- a/ports/unix/Makefile
+++ b/ports/unix/Makefile
@@ -90,6 +90,8 @@ ifeq ($(MICROPY_USE_READLINE),1)
 INC +=  -I$(TOP)/lib/mp-readline
 CFLAGS_MOD += -DMICROPY_USE_READLINE=1
 LIB_SRC_C_EXTRA += mp-readline/readline.c
+else
+LDFLAGS_MOD += -lreadline
 endif

--- a/ports/unix/mpconfigport.mk
+++ b/ports/unix/mpconfigport.mk
@@ -6,7 +6,7 @@ MICROPY_FORCE_32BIT = 0
 # This variable can take the following values:
 #  0 - no readline, just simple stdin input
 #  1 - use MicroPython version of readline
-MICROPY_USE_READLINE = 1
+MICROPY_USE_READLINE = 0
``` 

You must add micropython to the environments PATH variable:
```bash
$ export PATH="<path_to>/micropython/unix:$PATH"
```

## Stmhal port

You need to run some setup boilerplate code before you can run any micropython
code, see the examples directory::
```bash
$ import sys!!
$ sys.path.append('<path_to>/micropython/tools')!!
$ import pyboard!!
$ pyb = pyboard.Pyboard('<tty_device>')!!
```

The '!!' is how you run commands with the python 3 interpreter in Jupyter/Ipython. Any commands run without '!!' will be sent to the pyboard for processing

## Usage

mpkernel currently only supports running in the notebook
start the notebook server::

```bash
$ jupyter notebook
```

select either micropython-unix or micropython-stmhal from the drop down menu  

<!---
.. or
    run either kernel from the console::
    $ jupyter console --kernel=mpunix
    $ jupyter console --kernel=mpstmhal
-->

## Docker Dev Environment

```bash
# Build the docker image
$ make docker-build

# run the docker image
$ make docker-run
```

## Vagrant

run `vagrant up` from within this repository to create an mpkernel development
environment, with the latest micropython build

## Contributing

1. Fork it!
2. Create your feature branch: `git checkout -b my-new-feature`
3. Commit your changes: `git commit -am "Add some feature"`
4. Push to the branch: `git push origin my-new-feature`
5. Submit a pull request :D

## License

The MIT License (MIT)

Copyright (c) 2015 Tony Abboud

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.

<!---
.. _Python Package Index entry: http://pypi.python.org/pypi/mpkernel
-->
