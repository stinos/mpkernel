#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function
import os
import sys
import signal
from tornado.ioloop import IOLoop
from ipykernel.kernelbase import Kernel
from pexpect import replwrap, EOF

__version__ = '0.2'

try:
    from traitlets import Unicode
except ImportError:
    from IPython.utils.traitlets import Unicode


class MPKernelUnix(Kernel):
    """
    Kernel for the Unix Port of micropython
    """
    implementation = 'mpkernel'
    implementation_version = __version__
    banner = 'Welcome to the Unix port of MicroPython'
    language_info = {
                    'name': 'micropython',
                    'version': '3',
                    'codemirror_mode': {
                            'name': 'python',
                            'version': 3
                        },
                    'mimetype': 'text/x-python',
                    'file_extension': '.py',
                    'pygments_lexer': 'python3',
                    }

    def __init__(self, **kwargs):
        Kernel.__init__(self, **kwargs)
        self.start_interpreter()

    def start_interpreter(self):
        # Signal handlers are inherited by forked processes, we can't easily
        # reset it from the subprocess. Kernelapp ignores SIGINT except in
        # message handlers, we need to temporarily reset the SIGINT handler
        # so that bash and its children are interruptible.
        sig = signal.signal(signal.SIGINT, signal.SIG_DFL)
        try:
            self.interpreter = replwrap.REPLWrapper('micropython', u">>> ", None, u">>> ", u"... ")
        finally:
            signal.signal(signal.SIGINT, sig)

    def do_execute(self, code, silent, store_history=True,
                   user_expressions=None, allow_stdin=False):

        if not code.strip():
            return {
                'status': 'ok',
                'execution_count': self.execution_count,
                'payload': [],
                'user_expressions': {},
            }

        status = 'ok'
        traceback = None

        try:
            output = self.interpreter.run_command(code + '\n', timeout=5)
        except KeyboardInterrupt:
            self.interpreter.child.sendintr()
            status = 'interrupted'
            self.interpreter._expect_prompt()
            output = ''
        except ValueError:
            output = 'Incomplete input, restarting'
            self.start_interpreter()
        except EOF:
            output = 'Restarting MPKernelUnix'
            self.start_interpreter()
            status = 'error'
            traceback = []

        if not self.interpreter.child.isalive():
            self.log.error("MPKernelUnix interpreter died")
            loop = IOLoop.current()
            loop.add_callback(loop.stop)

        if not silent:
            # Send output on stdout
            stream_content = {'name': 'stdout', 'text': output}
            self.send_response(self.iopub_socket, 'stream', stream_content)

        reply = {
            'status': status,
            'execution_count': self.execution_count,
        }

        if status == 'interrupted':
            pass
        elif status == 'error':
            err = {
                'ename': 'ename',
                'evalue': 'evalue',
                'traceback': traceback,
            }
            self.send_response(self.iopub_socket, 'error', err)
            reply.update(err)
        elif status == 'ok':
            reply.update({
                'payload': [],
                'user_expressions': {},
            })
        else:
            raise ValueError("Invalid status: %r" % status)

        return reply

