# -*- coding: utf-8 -*-
#  Copyright 2011 Takeshi KOMIYA
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.

import functools
import os
import re
import sys
from io import StringIO
from shutil import rmtree
from tempfile import mkdtemp, mkstemp


def capture_stderr(func):
    def wrap(*args, **kwargs):
        try:
            stderr = sys.stderr
            sys.stderr = StringIO()

            func(*args, **kwargs)

            if re.search('(ERROR|Traceback)', sys.stderr.getvalue()):
                raise AssertionError('Caught error')
        finally:
            if sys.stderr.getvalue():
                print("---[ stderr ] ---")
                print(sys.stderr.getvalue())

            sys.stderr = stderr

    return functools.wraps(func)(wrap)


class TemporaryDirectory(object):
    def __init__(self, suffix='', prefix='tmp', dir=None):
        self.name = mkdtemp(suffix, prefix, dir)

    def __del__(self):
        self.clean()

    def clean(self):
        if os.path.exists(self.name):
            rmtree(self.name)

    def mkstemp(self, suffix='', prefix='tmp', text=False):
        return mkstemp(suffix, prefix, self.name, text)
