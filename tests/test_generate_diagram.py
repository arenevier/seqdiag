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

import pytest

import seqdiag.command
from utils import TemporaryDirectory, capture_stderr


def get_diagram_files(testdir):
    diagramsdir = os.path.join(testdir, 'diagrams')
    for file in os.listdir(diagramsdir):
        yield os.path.join(diagramsdir, file)


def get_fontpath(testdir):
    return os.path.join(testdir, 'VLGothic', 'VL-Gothic-Regular.ttf')


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


base_path = os.path.dirname(__file__)
generate_test_files = get_diagram_files(base_path)


@pytest.mark.parametrize("source", generate_test_files)
def test_generate(source):
    basepath = os.path.dirname(__file__)

    fontpath = get_fontpath(basepath)
    options = ['-f', fontpath]
    mainfunc = seqdiag.command.main
    generate(mainfunc, "svg", source, options)
