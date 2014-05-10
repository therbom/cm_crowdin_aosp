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

def purge_caf_additions(strings_base, strings_cm):
    # Load AOSP file and resources
    xml_base = minidom.parse(strings_base)
    list_base_string = xml_base.getElementsByTagName('string')
    list_base_string_array = xml_base.getElementsByTagName('string-array')
    list_base_plurals = xml_base.getElementsByTagName('plurals')
    # Load CM file and resources
    xml_cm = minidom.parse(strings_cm)
    list_cm_string = xml_cm.getElementsByTagName('string')
    list_cm_string_array = xml_cm.getElementsByTagName('string-array')
    list_cm_plurals = xml_cm.getElementsByTagName('plurals')
    with codecs.open(strings_cm, 'r', 'utf-8') as f:
        content = f.read()
    file_this = codecs.open('test.xml', 'w', 'utf-8')

    # All names from AOSP
    names_base_string = []
    names_base_string_array = []
    names_base_plurals = []

    # Get all names from AOSP
    for s in list_base_string :
        names_base_string.append(s.attributes['name'].value)
    for s in list_base_string_array :
        names_base_string_array.append(s.attributes['name'].value)
    for s in list_base_plurals :
        names_base_plurals.append(s.attributes['name'].value)

    # Get all names from CM
    for s in list_cm_string :
        name = s.attributes['name'].value
        if name not in names_base_string:
            content = re.sub(r'(<string name=\"' + name + '.*</string>)', r'', content)
            print name
            xml_cm.documentElement.removeChild(s)
    for s in list_cm_string_array :
        name = s.attributes['name'].value
        if name not in names_base_string_array:
            content = re.sub(r'(<string name=\"' + name + '.*</string>)', r'', content)
            print name
            xml_cm.documentElement.removeChild(s)
    for s in list_cm_plurals :
        content = re.sub(r'(<string name=\"' + name + '.*</string>)', r'', content)
        name = s.attributes['name'].value
        if name not in names_base_plurals:
            print name
            xml_cm.documentElement.removeChild(s)

    file_this.seek(0)
    file_this.truncate()
    file_this.write(content)
    file_this.close()

purge_caf_additions('strings_base.xml', 'strings_cm.xml')




print('Welcome to the CM Crowdin sync script!')

print('\nSTEP 0: Checking dependencies')
# Check for Ruby version of crowdin-cli
if subprocess.check_output(['rvm', 'all', 'do', 'gem', 'list', 'crowdin-cli', '-i']) == 'true':
    sys.exit('You have not installed crowdin-cli. Terminating.')
else:
    print('Found: crowdin-cli')
# Check for caf.xml
if not os.path.isfile('caf.xml'):
    sys.exit('You have no caf.xml. Terminating.')
else:
    print('Found: caf.xml')
# Check for android/default.xml
if not os.path.isfile('android/default.xml'):
    sys.exit('You have no android/default.xml. Terminating.')
else:
    print('Found: android/default.xml')
# Check for extra_packages.xml
if not os.path.isfile('extra_packages.xml'):
    sys.exit('You have no extra_packages.xml. Terminating.')
else:
    print('Found: extra_packages.xml')
# Check for repo
try:
    subprocess.check_output(['which', 'repo'])
except:
    sys.exit('You have not installed repo. Terminating.')
