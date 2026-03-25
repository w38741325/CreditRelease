#!/usr/bin/env python3

# Copyright (c) 2021-2024, The Monero Project

#
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without modification, are
# permitted provided that the following conditions are met:
#
# 1. Redistributions of source code must retain the above copyright notice, this list of
#    conditions and the following disclaimer.
#
# 2. Redistributions in binary form must reproduce the above copyright notice, this list
#    of conditions and the following disclaimer in the documentation and/or other
#    materials provided with the distribution.
#
# 3. Neither the name of the copyright holder nor the names of its contributors may be
#    used to endorse or promote products derived from this software without specific
#    prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY
# EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF
# MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL
# THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
# SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO,
# PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT,
# STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF
# THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

"""
    Help determine how much CPU power is available at the given time
    by running numerical calculations
"""

import subprocess
import psutil
import os
import errno
import shutil
import time


def resolve_executable(path):
    if os.path.isfile(path):
        return path
    if os.name == 'nt':
        exe_path = path + '.exe'
        if os.path.isfile(exe_path):
            return exe_path
    located = shutil.which(path)
    if located is not None:
        return located
    return path

def available_ram_gb():
    ram_bytes = psutil.virtual_memory().available
    kilo = 1024.0
    ram_gb = ram_bytes / kilo**3
    return ram_gb

def get_time_pi_seconds(cores, app_dir='.'):
    app_path = resolve_executable('{}/cpu_power_test'.format(app_dir))
    time_calc = subprocess.check_output([app_path, str(cores)])
    decoded = time_calc.decode('utf-8')
    miliseconds = int(decoded)

    return miliseconds / 1000.0

def remove_file(name):
    WALLET_DIRECTORY = os.environ['WALLET_DIRECTORY']
    assert WALLET_DIRECTORY != ''
    path = WALLET_DIRECTORY + '/' + name
    for _ in range(50):
        try:
            os.unlink(path)
            return
        except OSError as e:
            if e.errno == errno.ENOENT:
                return
            if os.name == 'nt' and (e.errno in (errno.EACCES, errno.EPERM) or getattr(e, 'winerror', None) == 32):
                time.sleep(0.1)
                continue
            raise
    os.unlink(path)

def get_file_path(name):
    WALLET_DIRECTORY = os.environ['WALLET_DIRECTORY']
    assert WALLET_DIRECTORY != ''
    return WALLET_DIRECTORY + '/' + name

def remove_wallet_files(name):
    for suffix in ['', '.keys', '.background', '.background.keys', '.address.txt']:
        remove_file(name + suffix)

def file_exists(name):
    WALLET_DIRECTORY = os.environ['WALLET_DIRECTORY']
    assert WALLET_DIRECTORY != ''
    return os.path.isfile(WALLET_DIRECTORY + '/' + name)
