# -*- coding: utf-8 -*-
#
# Copyright (C) 2009 Andrew Resch <andrewresch@gmail.com>
#
# This file is part of Deluge and is licensed under GNU General Public License 3.0, or later, with
# the additional special exception to link portions of this program with the OpenSSL library.
# See LICENSE for more details.
#

from __future__ import unicode_literals

import os.path

import pkg_resources


def get_resource(filename):
    return pkg_resources.resource_filename('deluge.plugins.execute',
                                           os.path.join('data', filename))
