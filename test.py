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
        content = [line.rstrip() for line in f]
    shutil.copyfile(strings_cm, strings_cm + '.backup')
    file_this = codecs.open(strings_cm, 'w', 'utf-8')

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
    content2 = []
    for s in list_cm_string :
        name = s.attributes['name'].value
        if name not in names_base_string:
            true = 0
            content2 = []
            for i in content:
                if true == 0:
                    test = re.search('(<string name=\"' + name + ')', i)
                    if test is not None:
                        test2 = re.search('(</string>)', i)
                        if test2:
                            true = 2
                        else:
                            true = 1
                        i = ''
                elif true == 1:
                    test2 = re.search('(</string>)', i)
                    if test2 is not None:
                        true = 2
                    i = ''
                elif true == 2:
                    print name
                    true = 3
                content2.append(i)
            content = content2
    for s in list_cm_string_array :
        name = s.attributes['name'].value
        if name not in names_base_string_array:
            true = 0
            content2 = []
            for i in content:
                if true == 0:
                    test = re.search('(<string-array name=\"' + name + ')', i)
                    if test is not None:
                        test2 = re.search('(</string-array>)', i)
                        if test2:
                            true = 2
                        else:
                            true = 1
                        i = ''
                elif true == 1:
                    test2 = re.search('(</string-array>)', i)
                    if test2 is not None:
                        true = 2
                    i = ''
                elif true == 2:
                    print name
                    true = 3
                content2.append(i)
            content = content2
    for s in list_cm_plurals :
        name = s.attributes['name'].value
        if name not in names_base_plurals:
            true = 0
            content2 = []
            for i in content:
                if true == 0:
                    test = re.search('(<plurals name=\"' + name + ')', i)
                    if test is not None:
                        test2 = re.search('(</plurals>)', i)
                        if test2:
                            true = 2
                        else:
                            true = 1
                        i = ''
                elif true == 1:
                    test2 = re.search('(</plurals>)', i)
                    if test2 is not None:
                        true = 2
                    i = ''
                elif true == 2:
                    # The actual purging is done!
                    print name
                    true = 3
                content2.append(i)
            content = content2

    for addition in content:
        file_this.write(addition + '\n')
    file_this.close()

# Load caf.xml
print('Loading caf.xml')
xml = minidom.parse('caf.xml')
items = xml.getElementsByTagName('item')

# Store all created cm_caf.xml files in here.
# Easier to remove them afterwards, as they cannot be committed
cm_caf = []

for item in items:
    # Create tmp dir for download of AOSP base file
    path_to_values = item.attributes["path"].value
    subprocess.call(['mkdir', '-p', 'tmp/' + path_to_values])
    for aosp_item in item.getElementsByTagName('aosp'):
        url = aosp_item.firstChild.nodeValue
        xml_file = aosp_item.attributes["file"].value
        path_to_base = 'tmp/' + path_to_values + '/' + xml_file
        path_to_cm = path_to_values + '/' + xml_file
        urlretrieve(url, path_to_base)
        purge_caf_additions(path_to_base, path_to_cm)
        cm_caf.append(path_to_cm)
        print('Purged ' + path_to_cm + ' from CAF additions')
'''
# Revert purges
for purged_file in cm_caf:
    os.remove(purged_file)
    shutil.copyfile(purged_file + '.backup', purged_file)
    print('Reverted purged file ' + purged_file)
'''
