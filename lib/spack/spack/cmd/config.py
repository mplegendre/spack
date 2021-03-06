##############################################################################
# Copyright (c) 2013, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Written by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://scalability-llnl.github.io/spack
# Please also see the LICENSE file for our notice and the LGPL.
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License (as published by
# the Free Software Foundation) version 2.1 dated February 1999.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the IMPLIED WARRANTY OF
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the terms and
# conditions of the GNU General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with this program; if not, write to the Free Software Foundation,
# Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA
##############################################################################
import sys
from external import argparse

import llnl.util.tty as tty

import spack.config

description = "Get and set configuration options."

def setup_parser(subparser):
    # User can only choose one
    scope_group = subparser.add_mutually_exclusive_group()
    scope_group.add_argument(
        '--user', action='store_const', const='user', dest='scope',
        help="Use config file in user home directory (default).")
    scope_group.add_argument(
        '--site', action='store_const', const='site', dest='scope',
        help="Use config file in spack prefix.")

    sp = subparser.add_subparsers(metavar='SUBCOMMAND', dest='config_command')

    set_parser = sp.add_parser('set', help='Set configuration values.')
    set_parser.add_argument('key', help="Key to set value for.")
    set_parser.add_argument('value', nargs='?', default=None,
                            help="Value to associate with key")

    get_parser = sp.add_parser('get', help='Get configuration values.')
    get_parser.add_argument('key', help="Key to get value for.")

    edit_parser = sp.add_parser('edit', help='Edit configuration file.')


def config_set(args):
    # default scope for writing is 'user'
    if not args.scope:
        args.scope = 'user'

    config = spack.config.get_config(args.scope)
    config.set_value(args.key, args.value)
    config.write()


def config_get(args):
    config = spack.config.get_config(args.scope)
    print config.get_value(args.key)


def config_edit(args):
    if not args.scope:
        args.scope = 'user'
    config_file = spack.config.get_filename(args.scope)
    spack.editor(config_file)


def config(parser, args):
    action = { 'set'  : config_set,
               'get'  : config_get,
               'edit' : config_edit }
    action[args.config_command](args)

