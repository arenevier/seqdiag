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

import os

from nose.tools import nottest

import seqdiag.command
from seqdiag.tests.utils import TemporaryDirectory, capture_stderr


def get_diagram_files(testdir):
    diagramsdir = os.path.join(testdir, 'diagrams')
    for file in os.listdir(diagramsdir):
        yield os.path.join(diagramsdir, file)


def get_fontpath(testdir):
    return os.path.join(testdir, 'VLGothic', 'VL-Gothic-Regular.ttf')


@nottest
def testcase_generator(basepath, mainfunc, files, options):
    fontpath = get_fontpath(basepath)
    options = options + ['-f', fontpath]

    for source in files:
        yield generate, mainfunc, 'svg', source, options


@capture_stderr
def generate(mainfunc, filetype, source, options):
    try:
        tmpdir = TemporaryDirectory()
        fd, tmpfile = tmpdir.mkstemp()
        os.close(fd)

        mainfunc(['--debug', '-T', filetype, '-o', tmpfile, source] +
                 list(options))
    finally:
        tmpdir.clean()


def test_generate():
    mainfunc = seqdiag.command.main
    basepath = os.path.dirname(__file__)
    files = get_diagram_files(basepath)
    options = []

    for testcase in testcase_generator(basepath, mainfunc, files, options):
        yield testcase
