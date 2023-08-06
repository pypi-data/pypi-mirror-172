from __future__ import absolute_import, division, print_function, unicode_literals
# Copyright (C) 2016 Red Hat, Inc.
# This file is part of libsan.
#
# libsan is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# libsan is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with libsan.  If not, see <http://www.gnu.org/licenses/>.


"""cmdline.py: Module to execute a command line."""

__author__ = "Bruno Goncalves"
__copyright__ = "Copyright (c) 2016 Red Hat, Inc. All rights reserved."

import subprocess
import sys


def run(cmd, return_output=False, verbose=True, force_flush=False):
    """Run a command line specified as cmd.
The arguments are:
\tcmd (str):    Command to be executed
\tverbose:      if we should show command output or not
\tforce_flush:  if we want to show command output while command is being executed. eg. hba_test run
\treturn_output (Boolean): Set to True if want output result to be returned as tuple. Default is False
Returns:
\tint: Return code of the command executed
\tstr: As tuple of return code if return_output is set to True
"""
    # by default print command output
    if verbose:
        # Append time information to command
        date = "date \"+%Y-%m-%d %H:%M:%S\""
        p = subprocess.Popen(date, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        stdout, stderr = p.communicate()
        stdout = stdout.decode('ascii', 'ignore')
        stdout = stdout.rstrip("\n")
        print("INFO: [%s] Running: '%s'..." % (stdout, cmd))

    stderr = b""
    if not force_flush:
        p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        stdout, stderr = p.communicate()
        sys.stdout.flush()
        sys.stderr.flush()
    else:
        p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)
        stdout = b""
        while p.poll() is None:
            new_data = p.stdout.readline()
            stdout += new_data
            if verbose:
                sys.stdout.write(new_data.decode('ascii', 'ignore'))
            sys.stdout.flush()

    retcode = p.returncode

    # print "stdout:(" + stdout + ")"
    # print "stderr:(" + stderr + ")"
    output = stdout.decode('ascii', 'ignore') + stderr.decode('ascii', 'ignore')

    # remove new line from last line
    output = output.rstrip()

    # by default print command output
    # if force_flush we already printed it
    if verbose and not force_flush:
        print(output)

    # print "stderr " + err
    # print "returncode: " + str(retcode)
    if not return_output:
        return retcode
    else:
        return retcode, output


def exists(cmd):
    rc = subprocess.call(['which', cmd])
    if rc == 0:
        return True
    else:
        return False
