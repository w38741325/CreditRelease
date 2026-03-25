#!/usr/bin/env python3

# Copyright (c) 2019-2024, The Monero Project
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

"""Test address validation RPC calls"""

import credit_fixtures as fixtures

from framework.wallet import Wallet


class AddressValidationTest():
    def run_test(self):
      self.create()
      self.check_bad_addresses()
      self.check_good_addresses()
      self.check_openalias_addresses()

    def create(self):
        print('Creating wallet')
        self.wallet = Wallet()
        # close the wallet if any, will throw if none is loaded
        try:
            self.wallet.close_wallet()
        except:
            pass
        res = self.wallet.restore_deterministic_wallet(seed=fixtures.SEED)
        assert res.address == fixtures.PRIMARY_ADDRESS
        assert res.seed == fixtures.SEED

    def check_bad_addresses(self):
        print('Validating bad addresses')
        bad_addresses = ['', 'a', fixtures.BAD_PRIMARY_ADDRESS, ' ', '@', fixtures.PRIMARY_ADDRESS[:5]]
        for address in bad_addresses:
            res = self.wallet.validate_address(address, any_net_type=False)
            assert not res.valid
            res = self.wallet.validate_address(address, any_net_type=True)
            assert not res.valid

    def check_good_addresses(self):
        print('Validating good addresses')
        for any_net_type in [True, False]:
            for address in fixtures.VALIDATE_ADDRESS_CASES:
                res = self.wallet.validate_address(address[2], any_net_type=any_net_type)
                if any_net_type or address[0] == 'mainnet':
                    assert res.valid
                    assert res.integrated == (address[1] == 'i')
                    assert res.subaddress == (address[1] == 's')
                    assert res.nettype == address[0]
                    assert res.openalias_address == ''
                else:
                    assert not res.valid

    def check_openalias_addresses(self):
        print('Validating openalias addresses')
        for allow_openalias in [False, True]:
            res = self.wallet.validate_address(fixtures.OPENALIAS_ALIAS, allow_openalias=allow_openalias)
            assert not res.valid
            assert not hasattr(res, 'openalias_address') or res.openalias_address == ''


if __name__ == '__main__':
    AddressValidationTest().run_test()
