#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Copyright (c) 2021 Jordi Mas i Hernandez <jmas@softcatala.org>
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this program; if not, write to the
# Free Software Foundation, Inc., 59 Temple Place - Suite 330,
# Boston, MA 02111-1307, USA.

from __future__ import print_function
import datetime
import os
import logging
import json

import sys
sys.path.append('../core/')

from optparse import OptionParser
from analyzer import Analyzer
from document import Document
from findfiles import FindFiles

def init_logging(del_logs):
    logfile = 'cli.log'

    if del_logs and os.path.isfile(logfile):
        os.remove(logfile)

    logger = logging.getLogger()
    hdlr = logging.FileHandler(logfile)
    logger.addHandler(hdlr)
    logger.setLevel(logging.DEBUG)

def read_parameters():
    parser = OptionParser()

    parser.add_option(
        '-f',
        '--file',
        type='string',
        action='store',
        default=None,
        dest='filename',
        help="File to process"
    )

    parser.add_option(
        '-d',
        '--directory',
        type='string',
        action='store',
        default=None,
        dest='directory',
        help="Directory to process"
    )

    parser.add_option(
        '-m',
        '--metrics',
        action='store_true',
        default=False,
        dest='metrics_only',
        help="Show metrics only"
    )

    (options, args) = parser.parse_args()

    if options.filename is None and options.directory is None:
        parser.error('Filename or directory not given')

    return options.filename, options.directory, options.metrics_only


def main():

    print("Runs metrics and rules on local file")
    print("Use --help for more details")

    init_logging(True)

    start_time = datetime.datetime.now()

    filename, directory, metrics_only = read_parameters()

    if filename is not None:
        files = [filename]
    else:
        findFiles = FindFiles()
        files = findFiles.find(directory, '*.txt')

    for file in files:
        document = Document()
        document.read_file(file)
        print(f"*** {file}")

        if metrics_only:
            results = Analyzer(document).get_metrics()
        else:
            results = Analyzer(document).get_all()

        json_results = json.dumps(results, ensure_ascii=False, indent=4, separators=(',', ': '))

        print(json_results)
    
    print("Time used: {0}".format(str(datetime.datetime.now() - start_time)))


if __name__ == "__main__":
    main()
