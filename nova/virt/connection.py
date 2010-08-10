# vim: tabstop=4 shiftwidth=4 softtabstop=4

# Copyright 2010 United States Government as represented by the
# Administrator of the National Aeronautics and Space Administration.
# All Rights Reserved.
# Copyright (c) 2010 Citrix Systems, Inc.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

"""Abstraction of the underlying virtualization API"""

import logging
import sys

from nova import flags
from nova.virt import fake
from nova.virt import libvirt_conn
from nova.virt import xenapi


FLAGS = flags.FLAGS


def get_connection(read_only=False):
    """Returns a connection to the underlying virtualization API
    
    The read_only parameter is passed through to the underlying API's
    get_connection() method if applicable
    """
    # TODO(termie): maybe lazy load after initial check for permissions
    # TODO(termie): check whether we can be disconnected
    t = FLAGS.connection_type
    if t == 'fake':
        conn = fake.get_connection(read_only)
    elif t == 'libvirt':
        conn = libvirt_conn.get_connection(read_only)
    elif t == 'xenapi':
        conn = xenapi.get_connection(read_only)
    else:
        raise Exception('Unknown connection type "%s"' % t)

    if conn is None:
        logging.error('Failed to open connection to the hypervisor')
        sys.exit(1)
    return conn
