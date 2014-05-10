#!/usr/bin/python2
# -*- coding: utf-8 -*-
# cm_crowdin_sync.py
#
# Updates Crowdin source translations and pulls translations
# directly to CyanogenMod's Git.
#
# Copyright (C) 2014 The CyanogenMod Project
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import codecs
import git
import mmap
import os
import os.path
import re
import shutil
import subprocess
import sys
from urllib import urlretrieve
from xml.dom import minidom

def set_correct_untranslatable(file_open):
    with codecs.open(file_open, 'r', 'utf-8') as f:
        content = [line.rstrip() for line in f]

    content2 = []

    for line in content:
        test = 0
        if test = 0:
            regex1 = re.search('(do not translate)', line, re.IGNORECASE)
            if regex1:
                test = 1
        else:
            regex2 = re.search('(name=\".*\")', line)
            if regex2:
                regex3 = re.search('([translatable|translate]=\"false\")', line, re.IGNORECASE)
                if regex3 is None:
                    line = re.sub('(name=\".*\")', '\1 translatable=\"false\"', line)
            test = 0
        content2.append(line)

    with codecs.open(file_open, 'w', 'utf-8') as f:
        for line in content2:
            f.write(line)
